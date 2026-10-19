# Default EOIP Web Application

React/Vite application used by the default Compose profile and main web CI. This is distinct from the TypeScript preview app under [frontend](../../frontend/README.md).

## Run and Build

From repository root with Node 22:

```powershell
npm --prefix apps/web ci
$env:EOIP_DEV_API_URL = 'http://127.0.0.1:8000'
npm --prefix apps/web run dev
```

Start the API separately using [Getting Started](../../docs/getting-started.md). The environment variable enables development proxying, not API startup. Vite prints the actual listening URL. Production `npm --prefix apps/web run build` emits static assets; the package Dockerfile/Containerfile serves them through `nginx.conf`, with same-origin API proxying and SPA fallback.

## Source Map

| Path | Responsibility |
|---|---|
| `src/App.jsx`, `main.jsx` | Application composition and explorer/query state |
| `src/app/` | Navigation, connection, shell and route error boundaries |
| `src/shared/api/` | API transport/policy helpers |
| `src/components/ui/`, `design-system/`, `icons.jsx` | Shared components, visual tokens and icons |
| `src/kgr/` | Graph views, renderers, analysis, workers and exports |
| `src/studio/` | Schema/query/connector/mapping/pipeline/system tools |
| `src/admin/` | Access, ingestion, quality, recovery and governance panels |
| `src/cognitive/`, `dashboards/` | Cognitive engineering and dashboard surfaces |

Some screens expose planned or profile-dependent capabilities. Check their real API calls and error handling before claiming completion. The current connection stores a token in memory and is not a suite-wide persistent SSO session.

## Checks and Change Rules

Run `typecheck`, `test:unit` and `build`. `test:e2e` and `test:a11y` run selected specs; review `playwright.config.js` and [Testing Guide](../../docs/testing-guide.md) before choosing live versus intercepted test profiles. Validate keyboard navigation, reduced motion, real graph rendering, loading/errors and exports in addition to compilation.

Reuse the existing client, components and policy behavior. Do not copy whole screens into new suite apps before the [frontend reconciliation](../../docs/frontend-development.md) and [suite migration](../../docs/EOIP-suite-architecture-plan.md) decisions.
