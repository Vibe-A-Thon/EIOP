# Preview Backend Shim

`server.py` is a supervisor/preview entry point that imports `apps.api.main:create_app` and exposes `app`. Its module documentation describes a supervisor invoking `uvicorn server:app` from this directory. It is not a separate backend implementation.

The shim adds the repository root to the import path, sets development defaults when absent, selects a local data directory and memory graph, and attempts to seed synthetic demo data. Its fallback API token is a development convenience, not an acceptable deployed credential. Do not expose it to untrusted networks.

For normal development/deployment use [Getting Started](../docs/getting-started.md) and `apps.api.main:create_app --factory` with explicit environment. Memory graph state is lost on restart, and the shim does not start the separate worker/MCP/frontend processes.

When refactoring, identify supervisor consumers before removing this entry point. Keep production changes in the real API/domain owners rather than adding independent logic here. Verify preview startup and fixture-seeding behavior separately from production authentication, persistence and release gates.
