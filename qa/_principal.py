"""Disposable QA principal (FT-AUTH).

The API has no default/bootstrap principal and ``EOIP_API_TOKEN`` is not registered by the server, so every
QA run that starts the application provisions the identity it uses: an ASG file (sha256 digest only, mode
0400) mapping a per-run random token to an explicit superadmin principal inside the run's disposable folder.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


def provision(root: str | os.PathLike, token: str, *, username: str = "qa-bench") -> dict[str, str]:
    """Write the ASG file under ``root`` and return the env vars that point the API at it."""
    folder = Path(root) / "qa-asg"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "asg.txt"
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    if path.exists():
        os.chmod(path, 0o600)
    path.write_text(f"sha256:{digest} | superadmin | * | {username}\n", encoding="utf-8")
    os.chmod(path, 0o400)
    return {"EOIP_ASG_FILE": str(path)}
