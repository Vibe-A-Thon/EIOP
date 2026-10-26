"""Shared disposable settings for local QA processes."""

from __future__ import annotations

import os
import secrets
from pathlib import Path


def environment(root: Path, inherited: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if inherited is None else inherited)
    env.update({
        "EOIP_DATA_DIR": str(root / "data"),
        "EOIP_GRAPH_BACKEND": "memory",
        "EOIP_API_TOKEN": secrets.token_urlsafe(32),
        "EOIP_ASG_FILE": str(root / "no-shared-credentials.keys"),
        "REVA_ENABLED": "false",
        "QA_REPORTS_DIR": str(root / "reports"),
    })
    return env
