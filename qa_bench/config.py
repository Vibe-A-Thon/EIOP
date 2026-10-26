"""Central Configuration for the EOIP / KnowGridFlow QA Automation Test Bench."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

REPO_ROOT = Path(__file__).resolve().parent.parent

# Safe runtime defaults for tests and standalone benchmarking
# No token defaults: tokens come from QA_BENCH_TOKEN_<ROLE> env vars mapped in your EOIP_ASG_FILE (FT-AUTH).
os.environ.setdefault("EOIP_GRAPH_BACKEND", "memory")
os.environ.setdefault("EOIP_DATA_DIR", str(REPO_ROOT / ".eoip-data"))

@dataclass(frozen=True)
class RoleCredential:
    label: str
    username: str
    role: str
    token: str
    tenant: str

# ASG token matrix: values are supplied per run via QA_BENCH_TOKEN_<ROLE> (never committed)
TEST_ROLES: dict[str, RoleCredential] = {
    "superadmin": RoleCredential(
        label="Super admin",
        username="root-superadmin",
        role="superadmin",
        token=os.environ.get("QA_BENCH_TOKEN_SUPERADMIN", ""),
        tenant="*",
    ),
    "admin": RoleCredential(
        label="Admin",
        username="default-admin",
        role="admin",
        token=os.environ.get("QA_BENCH_TOKEN_ADMIN", ""),
        tenant="default",
    ),
    "steward": RoleCredential(
        label="Steward",
        username="data-steward",
        role="steward",
        token=os.environ.get("QA_BENCH_TOKEN_STEWARD", ""),
        tenant="default",
    ),
    "analyst": RoleCredential(
        label="Analyst",
        username="analyst",
        role="analyst",
        token=os.environ.get("QA_BENCH_TOKEN_ANALYST", ""),
        tenant="default",
    ),
    "viewer": RoleCredential(
        label="Viewer",
        username="viewer",
        role="viewer",
        token=os.environ.get("QA_BENCH_TOKEN_VIEWER", ""),
        tenant="default",
    ),
    "bootstrap": RoleCredential(
        label="Bootstrap Root",
        username="bootstrap-root",
        role="admin",
        token=os.environ.get("QA_BENCH_TOKEN_BOOTSTRAP", ""),
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
