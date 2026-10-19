# Frontend Development and Reconciliation

There are two real frontend source trees. Neither should be removed merely because the other has a newer design. They do not currently share one runtime shell or auth client.

| Concern | `apps/web` | `frontend` |
|---|---|---|
| Entry | `src/main.jsx` and `src/App.jsx` | `src/main.tsx` and `src/App.tsx` |
| Router | App navigation/shell plus feature-local state | React Router screen routes |
| API transport | `src/shared/api/client.ts` | `src/lib/api.ts` |
| Design | Atlas CSS/tokens, shared components, Lucide, graph renderers | Tailwind/Vite, TypeScript UI components, Lucide, motion and Sigma |
| Development API | `EOIP_DEV_API_URL` configures proxy | `REACT_APP_BACKEND_URL` is a browser-visible API origin; no API proxy in its Vite config |
| Deployment reference | Default Compose and main web CI | Preview-oriented configuration; independently inspect its actual host |
| Scripts | dev, build, typecheck, unit, selected E2E/a11y | start/dev, build, preview, typecheck; no test script declared |

## Current UI Ownership

In `apps/web`, `App.jsx` hosts query/explorer views and lazy-loaded modules. `app/navigation.ts` declares top-level destinations. `studio/` combines schema/query/connectors/mapping/pipelines/systems. `admin/` combines access and operational controls. `kgr/` owns graph views, renderers, workers and analysis. `cognitive/` and `dashboards/` expose additional domain surfaces.

In `frontend`, `screens/` contains overview, Ask, graph, query, ontology, ingestion, agents, reports, governance, tenant, health, temporal and other screens; `shell/` owns the shell/navigation and `lib/` owns transport, auth and client state. Route existence is not proof that its backend workflow is complete.

## Working on the Default Web App

Use Node 22 and the existing lockfile:

```powershell
npm --prefix apps/web ci
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
```

Start the API as documented in [Getting Started](getting-started.md), then set `EOIP_DEV_API_URL` before `npm --prefix apps/web run dev`. Bind development servers to loopback for local work when appropriate. Do not put tokens in Vite variables.

For the alternate frontend, see its [README](../frontend/README.md). Its fixed preview settings include port 3000, permissive allowed-host configuration and HMR client port 443. Do not copy those settings into a hardened production deployment without review. Cross-origin API use requires deliberate server CORS configuration; disabling security is not a fix for a missing proxy.

## Security and State Limitations

The default web connection uses an in-memory token and describes deployment access. The alternate frontend's auth provider currently catches a failed identity lookup and constructs a bootstrap-admin UI principal. That behavior must not become the suite identity foundation. It does not prove the backend granted those privileges; the UI must not claim authenticated authority it has not established.

Treat tenant/principal headers as requested context, never as server authorization. Audit every cache key and async response for tenant/workspace/principal scope when changing auth. Log out and cancel/discard stale requests when context changes. Check direct endpoint access as well as hidden controls.

## Validation Before Merge

Run the selected package's actual scripts. For `apps/web`, browser configuration is [playwright.config.js](../apps/web/playwright.config.js). Its default base URL is container-oriented; host runs need `PLAYWRIGHT_BASE_URL`, and `EOIP_GUI_WEB_SERVER=1` enables its local Vite server. Check whether the selected spec uses intercepted fixtures or the real API before interpreting the result.

Test complete workflows with real services where required, then verify desktop/mobile screenshots, keyboard navigation, focus, reduced motion, error states, nonblank graphs, text fit and protected exports. Mock-backed component success does not establish backend integration.

When extracting a suite app, inventory both implementations, choose one owner, preserve unique behavior and route compatibility, and update shared contracts. Do not create a third design system or duplicate a backend engine in browser code.
