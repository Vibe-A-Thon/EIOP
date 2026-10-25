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

# Runtime configuration (FT-F02 / FT-AUTH). There is NO committed default token and NO
# default account. Principals are provisioned explicitly: EOIP_ADMIN_USERNAME +
# EOIP_ADMIN_PASSWORD(_FILE) create the first administrator (idempotent), and
# EOIP_API_TOKEN is honoured only when EOIP_API_TOKEN_ROLES maps it to a principal.
# Without any principal the app refuses to start (fail closed).
_DATA_DIR = Path(os.environ.get("EOIP_DATA_DIR") or (REPO_ROOT / ".eoip-data"))
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_DEV = os.environ.get("EOIP_ENV", "").strip().lower() == "dev"


def _provision_from_env() -> None:
    from eoip.authn.credentials import CredentialStore
    from eoip.authn.provision import provision_from_env

    store_path = os.environ.get("EOIP_CREDENTIALS_FILE") or _DATA_DIR / "state" / "credentials.json"
    provision_from_env(CredentialStore(store_path), log=lambda msg: print(msg, file=sys.stderr))


_provision_from_env()
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
