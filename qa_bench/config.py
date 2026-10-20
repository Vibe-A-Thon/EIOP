"""Central Configuration for the EOIP / KnowGridFlow QA Automation Test Bench."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

REPO_ROOT = Path(__file__).resolve().parent.parent

# Safe runtime defaults for tests and standalone benchmarking
os.environ.setdefault("EOIP_API_TOKEN", "eoip-local-dev-token-0123456789abcdef")
os.environ.setdefault("EOIP_GRAPH_BACKEND", "memory")
os.environ.setdefault("EOIP_DATA_DIR", str(REPO_ROOT / ".eoip-data"))

@dataclass(frozen=True)
class RoleCredential:
    label: str
    username: str
    role: str
    token: str
    tenant: str

# Standard ASG Token Matrix from Logins_credentials.keys
TEST_ROLES: dict[str, RoleCredential] = {
    "superadmin": RoleCredential(
        label="Super admin",
        username="root-superadmin",
        role="superadmin",
        token="eoip_sa_f86468fed910d947e69eba4c",
        tenant="*",
    ),
    "admin": RoleCredential(
        label="Admin",
        username="default-admin",
        role="admin",
        token="eoip_admin_75293814c25a2d4c1e57994c",
        tenant="default",
    ),
    "steward": RoleCredential(
        label="Steward",
        username="data-steward",
        role="steward",
        token="eoip_steward_449c1099ee3071aa8ce7fbed",
        tenant="default",
    ),
    "analyst": RoleCredential(
        label="Analyst",
        username="analyst",
        role="analyst",
        token="eoip_analyst_1d0019f09d075ddf8ad141dc",
        tenant="default",
    ),
    "viewer": RoleCredential(
        label="Viewer",
        username="viewer",
        role="viewer",
        token="eoip_viewer_9072655bae91c450d24fe204",
        tenant="default",
    ),
    "bootstrap": RoleCredential(
        label="Bootstrap Root",
        username="bootstrap-root",
        role="admin",
        token="eoip-local-dev-token-0123456789abcdef",
        tenant="default",
    ),
}

# Network URLs and Ports
BACKEND_URL: str = os.environ.get("EOIP_BACKEND_URL", "http://localhost:8001").rstrip("/")
FRONTEND_URL: str = os.environ.get("EOIP_FRONTEND_URL", "http://localhost:3000").rstrip("/")
API_PREFIX: str = "/api/v1"

# Driver & Browser Configuration
DEFAULT_BROWSER: str = os.environ.get("QA_BROWSER", "chrome").lower()
HEADLESS_MODE: bool = os.environ.get("QA_HEADLESS", "true").lower() in ("true", "1", "yes")
DEFAULT_TIMEOUT_SECS: float = float(os.environ.get("QA_TIMEOUT", "12.0"))

# Output Reports & Screenshots
REPORTS_DIR: Path = REPO_ROOT / "qa_bench" / "reports"
SCREENSHOTS_DIR: Path = REPORTS_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
