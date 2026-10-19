# Current State and Architecture Decisions

## Inspected Baseline

Read the complete 521-line [suite plan](../../../docs/EOIP-suite-architecture-plan.md) alongside the current manifests, application entry points, deployment configuration and maintenance guides. This is a targeted extraction assessment, not a new exhaustive product audit. Existing uncommitted changes in `packages/eoip/neural/antistub.py` were not modified.

| Current source | Observed boundary | Consequence for extraction |
|---|---|---|
| [API factory](../../../apps/api/main.py) and `app.py`, `extended.py`, `asg.py` | Imports `apps.api.*`, composes many domains | Moving only `main.py` is insufficient; preserve composition and security middleware |
| [Worker](../../../apps/worker/main.py) | Uses shared `eoip` modules and root-relative mapping paths | Needs a pinned platform distribution and explicit configuration/resource paths |
| [MCP](../../../apps/mcp/main.py) | Separate process, configured deployment token, default API container hostname | Package separately; retain bootstrap behavior without claiming multi-user delegated authorization |
| [Platform manifest](../../../pyproject.toml) | Distribution `eoip`; package discovery includes `eoip*` under `packages/` | API/worker applications and root REVA code are not automatically shipped in its wheel |
| [Runtime image](../../../deploy/Dockerfile) | Copies apps, config, demos, schemas and scripts outside the wheel | Must inventory non-Python resources; a wheel-only migration will omit runtime inputs |
| [Default Compose](../../../deploy/docker-compose.yml) | API/worker/MCP share one image and local data volume; default web is `apps/web` | Separate repository/image packaging must initially preserve qualified one-host state semantics |
| [Primary frontend](../../../apps/web/package.json) | React 19.1.1, Vite 7.3.6, TypeScript 5.9.3; type/unit/browser checks | Start from its tested build contract; do not assume alternate frontend dependencies match |
| [Alternate frontend](../../../frontend/package.json) | React 19.1.1, Vite 6 range, router/TanStack/Tailwind/Motion | Reconcile unique functionality and dependency versions before selecting shared components |
| [Alternate Vite configuration](../../../frontend/vite.config.ts) | Port 3000, permissive host setting, custom HMR port | Not a ready-made suite development configuration |
| [Extension](../../../apps/vscode-extension/package.json) | 19 commands; separately packaged; `/output` package path assumes its container | Keep one extension identity; revise packaging and test multi-root source navigation |
| [REVA guide](../../../reva/README.md) | Optional mount and documented initialization/packaging/identity caveats | Own a separate future package; do not copy completion claims into the suite release |
| [Test bootstrap](../../../tests/conftest.py) | Repository-root import/bootstrap assumptions | Extraction requires isolated test configuration, fixtures and resource ownership |

Existing CI pins Python 3.11 and Node 22.18.0 in its relevant jobs. Treat these as baseline reproduction values, not claims that they are the latest secure runtimes. Record reviewed exact toolchain versions per repository before the first independent build; update them in a separate validated change.

## Decisions Established by This Handbook

| ID | Decision | Reason and constraint |
|---|---|---|
| MULTI-D01 | One GitHub organization, `AvyukthiAI`; every application has its own private repository | Explicit latest user requirement and confirmed organization; changes the earlier repository recommendation |
| MULTI-D02 | Sibling clones plus a manifest and VS Code workspace; no default submodules | Independent Git operations, simpler daily work; reproducibility comes from pinned revisions |
| MULTI-D03 | `eoip-suite` is coordination, not another application monolith | Owns orchestration, workspace and suite releases; does not contain copies of application source |
| MULTI-D04 | Retain one logical backend platform initially | Repository separation must not fragment approval/dispatch authority or duplicate domain state |
| MULTI-D05 | Preserve distribution/import name `eoip` initially | A repository rename must not cause unnecessary package/API migration |
| MULTI-D06 | Use React/Vite and per-repository npm lockfiles | Reuse existing investment; no cross-repository npm workspace/hoisting requirement |
| MULTI-D07 | Use ordinary app navigation and independent builds first | No runtime module federation or remote script trust expansion without a separate requirement |
| MULTI-D08 | Start with coordinated suite releases | Independent repositories do not prove arbitrary version compatibility |
| MULTI-D09 | Same-origin customer portal paths, separate operator trust zones | Shared user experience does not eliminate domain authorization or isolate same-origin scripts |
| MULTI-D10 | All normative requirement IDs and evidence gates survive moves | File relocation is not requirement completion |

Technical defaults are specified so work can begin, and the user has confirmed `AvyukthiAI` as the organization. Administrator authority, identity-provider choice, entitlement policy and release authorization still require verification or the actual owner's recorded input. See [decision register](15-decisions-sources-and-handover.md). Do not silently guess those values.

## Runtime Shape

```text
Customer browser
  -> suite gateway / reviewed session boundary
     -> independently built portal assets
     -> existing compatible API contracts
        -> shared platform domains and graph adapters
        -> owned job / authority / evidence persistence

Ingestion worker -> same owned platform contracts and qualified stores
MCP / VS Code / CLI / SDK -> authenticated supported API interfaces
Operator browser -> separate restricted gateway/origin -> authorized controls
```

There is no portal-to-database access and no portal-to-portal source import. A report portal may use the same core API deployment as Query while remaining a distinct repository, image, release and user experience.

## Migration States

| State | Runtime | Source authority |
|---|---|---|
| B0 | Current monolith runtime | Existing checkout; new repositories contain only reviewed setup/foundation work |
| B1 | New Query/Explorer builds use legacy API | Migrated frontend slices have new owners; unmigrated slices remain in legacy |
| B2 | Packaged platform plus separately packaged API/worker/MCP | Exact package versions and resource bundles; no invisible legacy checkout dependency |
| B3 | Seven initial portals and channels form a verified suite | Release manifest selects compatible component artifacts |
| B4 | Later specialist applications, selective service extraction | Each added boundary passes owning programme and operational gates |

At every cutover record the authoritative repository and old consumer disposition. Do not maintain permanent writable copies in old and new repositories. A temporary backport policy must name an owner, direction, cutoff and verification gate.
