"""Central Configuration for the EOIP / KnowGridFlow QA Automation Test Bench."""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from dataclasses import dataclass

REPO_ROOT = Path(__file__).resolve().parent.parent

# Safe runtime defaults for tests and standalone benchmarking

@dataclass(frozen=True)
class RoleCredential:
    label: str
    username: str
    role: str
    token: str
    tenant: str

# Disposable local roles; remote runs require explicitly supplied QA_TOKEN_* values.
TEST_ROLES: dict[str, RoleCredential] = {
    "superadmin": RoleCredential(
        label="Super admin",
        username="root-superadmin",
        role="superadmin",
        token=os.getenv("QA_TOKEN_SUPERADMIN") or secrets.token_urlsafe(32),
        tenant="*",
    ),
    "admin": RoleCredential(
        label="Admin",
        username="default-admin",
        role="admin",
        token=os.getenv("QA_TOKEN_ADMIN") or secrets.token_urlsafe(32),
        tenant="default",
    ),
    "steward": RoleCredential(
        label="Steward",
        username="data-steward",
        role="steward",
        token=os.getenv("QA_TOKEN_STEWARD") or secrets.token_urlsafe(32),
        tenant="default",
    ),
    "analyst": RoleCredential(
        label="Analyst",
        username="analyst",
        role="analyst",
        token=os.getenv("QA_TOKEN_ANALYST") or secrets.token_urlsafe(32),
        tenant="default",
    ),
    "viewer": RoleCredential(
        label="Viewer",
        username="viewer",
        role="viewer",
        token=os.getenv("QA_TOKEN_VIEWER") or secrets.token_urlsafe(32),
        tenant="default",
    ),
    "bootstrap": RoleCredential(
        label="Bootstrap Root",
        username="bootstrap-root",
        role="admin",
        token=secrets.token_urlsafe(32),
        tenant="default",
    ),
}

# Network URLs and Ports
BACKEND_URL: str = os.environ.get("EOIP_BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
FRONTEND_URL: str = os.environ.get("EOIP_FRONTEND_URL", "http://127.0.0.1:8080").rstrip("/")
API_PREFIX: str = "/api/v1"

# Driver & Browser Configuration
DEFAULT_BROWSER: str = os.environ.get("QA_BROWSER", "chrome").lower()
HEADLESS_MODE: bool = os.environ.get("QA_HEADLESS", "true").lower() in ("true", "1", "yes")
DEFAULT_TIMEOUT_SECS: float = float(os.environ.get("QA_TIMEOUT", "12.0"))

# Output Reports & Screenshots
REPORTS_DIR = Path(os.getenv("QA_REPORTS_DIR", str(REPO_ROOT / "test-results" / "qa-bench" / "legacy")))
SCREENSHOTS_DIR: Path = REPORTS_DIR / "screenshots"
