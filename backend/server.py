"""Supervisor entrypoint shim.

The Emergent platform's supervisor runs `uvicorn server:app` from /app/backend on
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

# Local-first runtime configuration. These are safe development defaults for the
# preview environment; production deployments inject their own values.
_DATA_DIR = REPO_ROOT / ".eoip-data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("EOIP_API_TOKEN", "eoip-local-dev-token-0123456789abcdef")
os.environ.setdefault("EOIP_DATA_DIR", str(_DATA_DIR))
os.environ.setdefault("EOIP_GRAPH_BACKEND", "memory")
os.environ.setdefault("EOIP_LOAD_DEMO", "true")

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
