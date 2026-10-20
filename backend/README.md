# Preview Backend Shim

`server.py` is a supervisor/preview entry point that imports `apps.api.main:create_app` and exposes `app`. Its module documentation describes a supervisor invoking `uvicorn server:app` from this directory. It is not a separate backend implementation.

The shim adds the repository root to the import path, selects a local data directory and memory graph, and (in the dev profile) seeds synthetic demo data.

**Credentials (FT-F02).** There is no committed fallback token. The supervisor/preview must inject `EOIP_API_TOKEN` (32+ characters) from its secret settings; without it the shim exits with an error. For local development only, set `EOIP_ENV=dev`: the shim then generates an ephemeral per-process token, writes it to `<EOIP_DATA_DIR>/dev-token` (mode 0600) and never prints it. `EOIP_LOAD_DEMO` defaults to `true` only in the dev profile. Extra principals come from an `EOIP_ASG_FILE` kept outside the repository (template: `Logins_credentials.keys.example`).

For normal development/deployment use [Getting Started](../docs/getting-started.md) and `apps.api.main:create_app --factory` with explicit environment. Memory graph state is lost on restart, and the shim does not start the separate worker/MCP/frontend processes.

When refactoring, identify supervisor consumers before removing this entry point. Keep production changes in the real API/domain owners rather than adding independent logic here. Verify preview startup and fixture-seeding behavior separately from production authentication, persistence and release gates.
