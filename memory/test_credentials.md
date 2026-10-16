# Test Credentials — KnowGridFlow / EOIP

Auth is token-based (Authorization: Bearer <token>). Tokens are held in-memory in
the browser; the ASG registry is defined in `/app/Logins_credentials.keys` and
enforced server-side (RBAC). Sign-in: /signin → paste a token → Continue.
The sign-in screen pre-fills the Super admin token and has quick-pick role buttons.

## ASG demo tokens (role · tenant)
- Super admin (full control, all tenants): `eoip_sa_f86468fed910d947e69eba4c`
- Admin (default tenant):                  `eoip_admin_75293814c25a2d4c1e57994c`
- Steward (default tenant):                `eoip_steward_449c1099ee3071aa8ce7fbed`
- Analyst (default tenant):                `eoip_analyst_1d0019f09d075ddf8ad141dc`
- Viewer (default tenant):                 `eoip_viewer_9072655bae91c450d24fe204`

## Fail-safe bootstrap superadmin (recovery)
- Env `EOIP_API_TOKEN` (currently `eoip-local-dev-token-0123456789abcdef`) is ALWAYS
  registered as a superadmin even if the keys file is missing/empty — cannot be
  locked out. Works as a Bearer token exactly like the Super admin above.

## RBAC expectations (server-enforced)
- Reads (GET): any valid token → 200; invalid/none → 401.
- Destructive ops require admin/system/superadmin → others get 403:
  ontology gitops merge/rollback/package-release/migration, marketplace install/
  build/uninstall, enterprise snapshots create/restore/delete, ontology import.
- Tenant isolation: a tenant-bound principal cannot read/act on another tenant
  (e.g. branding/theme?tenant_id=<other> → 403). Only superadmin is cross-tenant.
- Admin-only nav (Governance, Brand, Tenant) is hidden for non-admin roles in the UI.

## Key data-testids
- signin: signin-token-input, signin-tenant-input, signin-submit-button,
  signin-demo-roles, signin-role-super-admin/-admin/-steward/-analyst/-viewer
- shell: app-shell-nav-rail, app-shell-nav-<id>, app-shell-rail-toggle
- In-app navigation: after sign-in, navigate via left-rail <a href> links
  (full page reloads drop the in-memory token and bounce to /signin).

## Tenant
- Default tenant id: `default` (maps to the seeded demo graph).
