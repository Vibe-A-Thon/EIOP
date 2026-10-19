# Alternate TypeScript Frontend

This is a substantial React/TypeScript application, not an empty placeholder. It has its own routing, shell, API client and auth state. The default repository Compose stack and main web CI target `apps/web`, so changes here do not automatically update that deployed UI.

## Structure

`src/App.tsx` registers the screens. `screens/` includes overview, Ask, graph/entity, query, ingestion, ontology, quality, agents, reports, governance, tenancy, health and temporal views. `shell/` owns navigation/panels. `lib/api.ts` and `lib/auth.tsx` own this frontend's transport/auth state. `components/` and `index.css` contain its reusable visual layer.

## Development Prerequisites

Inspect `package.json` and its lockfile policy before dependency installation. This tree currently declares `start`, `dev`, `build`, `preview` and `typecheck`; it does not declare the default web app's test scripts. Use `npm --prefix frontend install` when no committed compatible lockfile exists; review any generated lockfile rather than silently changing other packages.

`REACT_APP_BACKEND_URL` selects the browser-visible API origin. It is not a secret and is read at build/dev-server startup. The API client appends `/api/v1`; do not include that prefix twice. Without the setting it uses the browser origin, which requires the hosting proxy to route `/api/v1` to the API.

```powershell
$env:REACT_APP_BACKEND_URL = 'http://127.0.0.1:8000'
npm --prefix frontend run dev
```

Cross-origin use also requires a deliberately configured API CORS policy. `vite.config.ts` has preview-oriented port 3000, `strictPort`, permissive hosts and HMR client port 443. These are not hardened deployment defaults and may need a profile-specific configuration for host development. Do not assume the `apps/web` proxy variable works here.

## Known Boundary to Resolve

`lib/auth.tsx` currently catches identity lookup failure and constructs a bootstrap-admin UI principal. Treat this as a known adoption blocker for suite identity, not evidence of authenticated authority. Backend authorization must be tested independently. Tokens live in memory; there is no basis to promise seamless persistent cross-app SSO.

Run `npm --prefix frontend run typecheck` and `npm --prefix frontend run build` after changes, and add/test the actual workflow using the intended backend. Reconcile unique behavior against `apps/web` before either frontend is retired. See [Frontend Development](../docs/frontend-development.md).
