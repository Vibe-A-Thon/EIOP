# Repository Implementation Templates

These are target repository contracts. Materialize only the selected repository type, replacing placeholders and implementing real behavior. An empty scaffold is `planned` or `in progress`, never a completed application.

## Common Files

```text
README.md
LICENSE
NOTICE
LICENSING.md
THIRD_PARTY_NOTICES.md
licenses/                         only applicable first/third-party material
.gitignore
.editorconfig
AGENTS.md                         repository-specific implementation boundaries
.github/CODEOWNERS
.github/pull_request_template.md
.github/workflows/ci.yml
docs/architecture.md
docs/configuration.md
docs/runbook.md
docs/verification.md
tests/
```

Review which existing legal files apply rather than copying unrelated legal schedules. No new license text is drafted by this handbook. Never strip notices from extracted third-party material.

README must state purpose/non-goals, artifact, supported runtime/profile, exact install/run/test commands, environment names/defaults, secret provisioning, persistence, dependencies, API boundaries, failure behavior, evidence status, maintainer and migration/rollback. New commands must be backed by executable code and observed results before advertised as working.

Ignore `.venv/`, `node_modules/`, local `.env` variants except reviewed `.env.example`, build/test output, `.local/`, local certificates, runtime databases and raw evidence. Ignore patterns do not remove previously tracked files; review tracked state separately without deleting historical fixtures needed by existing tests.

## Browser Application

```text
src/
  app/                            bootstrap, routes, capability wiring
  features/<owned-workflow>/       screens, state and API integration
  components/                     app-specific presentation only
  test/                           test support; no production fake success
public/                           reviewed static assets
tests/unit/
tests/browser/
tests/contracts/
package.json
package-lock.json
tsconfig.json
vite.config.ts
playwright.config.ts
app.manifest.json
Dockerfile
.vscode/tasks.json
```

Start by reconciling the existing JSX/TS implementations; do not convert every existing file to TypeScript solely to split repositories. New boundaries/types should be explicit. Keep each app's own npm lockfile. Shared UI dependencies are versioned packages, not copied source.

Required scripts: `dev`, `build`, `typecheck`, `test:unit`, `test:browser`, `test:a11y`, `validate`. `validate` executes actual type, unit and build checks and propagates failures. Browser/a11y checks run against their declared real or isolated component environment and report which; release checks use real backend journeys. Do not use `--if-present`, `echo success`, empty test globs or mock-only tests as release gates.

Illustrative app manifest before artifact publication:

```json
{
  "schemaVersion": 1,
  "appId": "APP-05",
  "repository": "eoip-query-portal",
  "routeRoot": "/query/",
  "trustZone": "customer",
  "ownerRole": "query-maintainer",
  "requiredCapabilities": ["query.read"],
  "releaseStatus": "not-qualified",
  "artifact": null,
  "apiContractVersion": null,
  "offlineQualified": false
}
```

The release generator fills validated artifact/contract values from build outputs; nulls prohibit production activation. Capability names are target catalog identifiers and must be mapped to actual server capabilities, not inferred from route existence. Server authorization remains independent of app visibility.

UX acceptance covers loading, empty, denied, unavailable, stale, partial, cancelled and failed states; responsive density; focus and keyboard traversal; reduced motion; usable graph/table rendering; consistent shell; no explanatory placeholder cards masquerading as features. Reuse shared Lucide icons/tokens and current domain semantics.

## Python Service: API, Worker or MCP

```text
src/eoip_api/                     or eoip_worker / eoip_mcp
  __init__.py
  main.py
tests/unit/
tests/contracts/
tests/integration/
pyproject.toml
requirements-runtime.lock         generated for this artifact/profile
requirements-dev.lock
Dockerfile
.vscode/launch.json
```

Target API command after extraction is `python -m uvicorn eoip_api.main:create_app --factory --host 127.0.0.1 --port 8000`; MCP uses `eoip_mcp.main:create_app` on 8001; worker uses `python -m eoip_worker.main` only after a tested executable module is provided. These commands do **not** exist in the current checkout under those names.

Declare the platform version and every direct runtime dependency. Avoid importing another application's internals. Preserve current security middleware and job semantics. Add readiness that checks actual dependencies without exposing secrets; a successful Python import is not service readiness. Include graceful shutdown, configuration validation, structured error handling and diagnostic correlation.

Every service must build/install its wheel without the source tree, run as an unprivileged container user, declare writable paths explicitly and keep secrets out of image layers/build arguments. Test missing package resources, missing credentials, unreachable stores, restart and shutdown. Pin base image and dependency artifacts at release.

## Platform Library

Keep public imports `eoip.*` stable while moving the distribution to `eoip-platform`. Begin with the existing package layout if it reduces migration risk; a move to `src/` is not required. Unit tests and resource-loading tests follow their domains. Add installed-wheel acceptance outside source cwd. Record public versus internal interfaces and prohibit app-startup dependencies.

## MCP and VS Code Specifics

MCP must preserve existing tool names, bounds, errors and the declared local token profile while independently qualifying any remote authorization change. Test protocol initialization, discovery, invocation, cancellation/error transport and denied access using a real supported client. Do not derive authority from a tool's read-only annotation.

VS Code preserves publisher/extension/command identity unless an explicit migration is approved. Move its whole package with tests and fixtures; replace the `/output`-only packaging assumption with a portable `dist` output contract. Verify extension host behavior on Windows and the declared supported platforms. Do not create a second extension to avoid migration of stored settings and secrets.

## Engineering and Verification Repositories

`eoip-engineering` preserves normative requirement IDs and authoritative source links. Move specifications with a relocation map; maintain links from the legacy docs during transition. Historical reports retain original dates and evidence identity.

`eoip-verification` accepts a suite manifest/profile, provisions isolated state, runs real journeys and emits evidence with source/artifact identities. Keep runner credentials separate from application credentials. Missing artifacts, skips, stale evidence or mismatched digests must prevent a verified result.

## Coordination Repository

```text
eoip-suite/
  repos.json
  suite.lock.json
  eoip-suite.code-workspace
  profiles/
  compose/
  releases/
  scripts/                         validated bootstrap/start/stop/doctor tools
  .github/workflows/               pinned reusable CI and suite assembly
  docs/
```

The tooling must support dry-run/inspection, safe re-execution, meaningful exit codes and explicit destructive-operation boundaries. It must not silently install global tools, reset dirty repos, overwrite configuration, print tokens or treat all repositories' current HEADs as a qualified release.
