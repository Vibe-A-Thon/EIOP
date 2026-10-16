# KnowGridFlow / EOIP — GUI Rebuild PRD

## Original problem statement
Rebuild the project's GUI from scratch (the old one was "childish / a mess"), following
`GUI-cc-ghcp-requirements.md` exactly in intent: a calm, modular, evidence-first enterprise
ontology & knowledge-graph workbench, integrated with the REAL backend API (no mock data),
with best-in-class graphics, transitions, animations, icons, and modular screens.

## User choices (gathered 2026-06)
- First slice: most impactful end-to-end evidence-first demo path.
- Backend: stand up the real `apps/api` EOIP FastAPI so the GUI uses real `/api/v1/*` data.
- Design: a FRESH distinctive look (not a literal copy of the spec tokens) — produced via design agent
  ("Swiss High-Density Data Workbench").
- Stack: bound stack where it matters, pragmatic simplifications allowed.
- Local-first; no external integration keys.

## Architecture (as built)
- **Backend**: real `eoip` package (587 py files). Served on :8001 via `/app/backend/server.py`
  (supervisor-managed) which re-exports `apps.api.main:create_app`. Config: `EOIP_GRAPH_BACKEND=memory`,
  demo corpus seeded on startup (~226 vertices / 721 edges). Bootstrap token auth.
  - Minimal edit to `apps/api/main.py`: added `app.state.store = store` so the shim can seed demo data.
- **Frontend**: NEW app in `/app/frontend` (served on :3000 via `yarn start` → Vite).
  Stack: React 19 + TypeScript (strict) + Vite + TanStack Query + Zustand + react-router-dom +
  Tailwind v4 (CSS-variable 4-theme system) + Lucide icons + framer-motion + Sigma/Graphology (WebGL graph) +
  @fontsource (Outfit / IBM Plex Sans / JetBrains Mono, bundled = local-first).
- Token + tenant held in memory only (spec R5). All API calls prefixed `/api/v1`, with
  Authorization / X-Tenant-Id / X-Correlation-ID headers.

## Design system
`/app/design_guidelines.json` — 4 themes (dark / light / hc-dark / hc-light), six fact-class colors
(Deterministic/Derived/Inferred/Ambiguous/Human-confirmed/Unknown), semantic status colors, crisp
1px-border flat elevation, bounded motion, data-testid conventions.

## Implemented (2026-06) — verified by testing agent at 100% frontend
- **App Shell**: collapsible nav rail, top context bar (tenant/workspace, backend status chip,
  global search, command palette, theme switcher, principal menu + sign out), right inspector drawer,
  bottom activity dock (polls `/graph/events`, "Live updates: polling").
- **SCR-001 Sign-in**: dual-panel; token (in-memory) + tenant; verify via `/security/tokens/verify`
  with bootstrap fallback; identity-provider health chip.
- **SCR-003 Overview**: real stat tiles (vertices/edges/density/labels), graph-by-domain distribution,
  three independent system signals (never one %), recent activity.
- **SCR-004 Ask**: NL query via `/query/nl`, answer-mode badge (Deterministic/Narrated/…),
  boundary badge ("Local only" from `/egress/endpoints`), matched entities, evidence, suggestion chips, follow-ups.
- **SCR-005 Graph Explorer**: Sigma WebGL graph; auto-discovers the most-connected hub
  (`/search` + `/graph/metrics` → `/neighborhood`, ~52 nodes); domain/fact lens switcher, legend,
  fact-class filters, seed search, expand/reset, click-to-inspect.
- **SCR-006 Entity 360**: tabs Overview (properties + centrality), Relationships (in/out edges),
  Provenance (`/lineage`), Impact (`/graph/blast-radius` with risk + by-depth bars), Raw JSON.
- **Schema**: ontology/schema versions, domains, vertex/edge label tables with instance counts + search.
- **Command palette** (⌘K): live entity search + navigation.

## Implemented (2026-06, iteration 2) — verified by testing agent at 100%
- **Narrated streamed answers (Ask)**: Answer-mode toggle (Deterministic | Narrated). Narrated mode runs
  `/query/nl` for grounding (matched entities + numbered "Grounding evidence" with hover) and streams a
  live narration from `/brain/llm/stream` (SSE over POST) with a Stop button, client-side pacing, and
  "Simulated (not model inference)" badge + footnote (deployment model is the simulator).
- **Impact Paths (Graph Explorer)**: Explore | Impact-paths mode. Pick source + target entities, trace via
  `/graph/shortest-paths`; renders a path subgraph + a paths-list panel (sequence chips → inspector).
- **Saved Views (Graph Explorer)**: Save/open/delete named views (seeds + lens + fact filters) in
  localStorage, namespaced `{principal, tenant, workspace}`, labeled "Saved on this device only".
- **Ingestion Console (/ingestion)**: tabs — Ingestion runs (`/ingestion/runs`), Jobs (`/admin/jobs`,
  cancel/readmit), Sources (`/sources` + 16-connector catalog from `/connectors/catalog`), DLQ (`/admin/dlq`).

## Implemented (2026-06, iteration 3) — verified by testing agent (4/4 features)
- **Path Highlight on neighborhood**: Impact-paths now merges both endpoints' neighborhoods and
  highlights the traced path (bright nodes + cyan edges) while dimming context, via a Sigma decoration
  effect in `GraphCanvas` (`highlightNodes`/`highlightEdges`). Switching to Explore clears it.
- **Evidence Pinning**: Pin buttons on Ask evidence items push snippets to a right-side "Evidence board"
  drawer (zustand `pinsStore`), with top-bar count badge, copy, export-JSON, remove, and clear.
- **Source Onboarding**: 3-step wizard (details → review → create via `POST /sources`, then
  `POST /sources/{id}/baseline`) launched from any connector card in the Ingestion Console. URL-type
  connectors (api/crawler/web) require a base URL (client-side guard; prevents backend 422).
- **View Sharing**: Export all saved graph views to JSON and import them back (`exportViews`/`importViews`),
  for team collaboration; footnote "Saved on this device only. Export to share with teammates."

## Prioritized backlog (next)
- P1: Within-context path highlight toggle (overlay vs isolated subgraph).
- P2: Reports (SCR-019), Governance/Security (SCR-021), Tenant admin (SCR-022), Health (SCR-024).
- P2: Full WCAG 2.2 AA audit (axe), ICU string externalization, screen-reader transcripts.
- P2: Replace react-router-dom with TanStack Router for typed deep links `/t/:tenant/w/:workspace/...`.

## Notes
- No external keys; local-first. Backend graph store is in-memory (ephemeral; reseeded on restart).
- Auth is memory-only, so a hard refresh returns to /signin (expected per spec R5).
