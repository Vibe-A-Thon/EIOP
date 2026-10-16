# Test Credentials — KnowGridFlow GUI

## App URLs
- Frontend (preview): https://a832c397-f166-433b-a538-c85d71fb17f9.preview.emergentagent.com
- Backend API base: `${REACT_APP_BACKEND_URL}/api/v1` (routes through ingress to port 8001)

## Authentication (SCR-001 Sign-in)
The GUI authenticates with a Bearer access token held in memory only (no localStorage).

- **Access token (bootstrap deployment admin):** `eoip-local-dev-token-0123456789abcdef`
- **Tenant:** `default`
- The sign-in form at `/signin` pre-fills this token. Enter token → Continue.
- This bootstrap token maps to principal `bootstrap-admin` with roles `admin, system`.

## Backend
- EOIP FastAPI app served via `/app/backend/server.py` (re-exports `apps.api.main:create_app`).
- Graph backend: in-memory (`EOIP_GRAPH_BACKEND=memory`), seeded with the core demo corpus
  on startup (~226 vertices / ~721 edges).
- No external API keys required (local-first).

## data-testid highlights
- signin-token-input, signin-tenant-input, signin-submit-button
- app-shell-nav-overview / -ask / -graph / -schema, app-shell-rail-toggle
- global-search-trigger, command-palette-trigger, command-palette-input, command-palette-result
- tenant-select-dropdown, backend-status-chip, theme-toggle-button, theme-option-*, principal-menu-trigger, signout-button
- overview-ask-cta
- ask-query-input, ask-submit-button, ask-boundary-badge, ask-suggestion-*, ask-result
- graph-seed-search, graph-seed-result, graph-lens-domain / -fact, graph-expand-selected, graph-reset, graph-canvas, graph-filter-*
- entity-360, entity-tab-overview/-relationships/-provenance/-impact/-raw
- inspector-panel, inspector-close, inspector-open-full
- activity-dock, activity-dock-toggle
- schema-tab-vertex/-edge, schema-search
