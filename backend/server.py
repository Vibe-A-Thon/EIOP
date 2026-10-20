"""Supervisor entrypoint shim.

The eoip platform's supervisor runs `uvicorn server:app` from /app/backend on
port 8001. The real application is the EOIP FastAPI app defined in /app/apps/api.
This shim wires the environment and re-exports that app as `app`.
"""

import os
import sys
from pathlib import Path

# Make the repository root importable (eoip is pip-installed editable, apps is not).
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Runtime configuration (FT-F02). There is NO committed default token: the
# supervisor/preview must inject EOIP_API_TOKEN from its secret settings. Only an
# explicit development profile (EOIP_ENV=dev) gets an ephemeral per-process token,
# written to <data dir>/dev-token with mode 0600 and never printed.
_DATA_DIR = Path(os.environ.get("EOIP_DATA_DIR") or (REPO_ROOT / ".eoip-data"))
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_DEV = os.environ.get("EOIP_ENV", "").strip().lower() == "dev"


def _ensure_api_token() -> None:
    if os.environ.get("EOIP_API_TOKEN"):
        return
    if not _DEV:
        raise SystemExit(
            "EOIP_API_TOKEN is required (inject it from the secret store); "
            "set EOIP_ENV=dev for an ephemeral local development token"
        )
    import secrets

    token = secrets.token_urlsafe(32)
    token_file = _DATA_DIR / "dev-token"
    fd = os.open(token_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(token)
    os.chmod(token_file, 0o600)
    os.environ["EOIP_API_TOKEN"] = token
    print(f"[server] EOIP_ENV=dev: ephemeral API token written to {token_file} (mode 0600)", file=sys.stderr)


_ensure_api_token()
os.environ.setdefault("EOIP_DATA_DIR", str(_DATA_DIR))
os.environ.setdefault("EOIP_GRAPH_BACKEND", "memory")
os.environ.setdefault("EOIP_LOAD_DEMO", "true" if _DEV else "false")

from apps.api.main import create_app  # noqa: E402

app = create_app()


def _seed_demo_graph() -> None:
    """Populate the in-memory graph with the core demo corpus on startup."""
    try:
        store = app.state.store
        if getattr(store, "count_vertices", lambda: 0)() > 0:
            return
        from eoip.demo import load_demo

        load_demo(store, Path(os.environ["EOIP_DATA_DIR"]), project_root=REPO_ROOT)
    except Exception as exc:  # pragma: no cover - best-effort seed
        print(f"[server] demo seed skipped: {exc}", file=sys.stderr)


_seed_demo_graph()
