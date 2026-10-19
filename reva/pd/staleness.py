"""Owner digest staleness monitor and change tracking (T-213 / REVA-PD-007)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from reva.pd.bindings import Binding
from reva.pd.owner_digest import compute_owner_digest


def detect_stale_obligations(
    bindings: List[Binding],
    repo_path: Union[str, Path],
    from_commit: Optional[str] = None,
    to_commit: Optional[str] = "HEAD",
) -> List[Tuple[str, str, str]]:
    """Identify obligations whose code owners have changed or drifted in digest.
    
    Returns list of tuples: (obligation_key, owner_path, reason)
    """
    repo = Path(repo_path).resolve()
    changed_files: Optional[Set[str]] = None

    if from_commit and to_commit:
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo), "diff", "--name-only", from_commit, to_commit],
                capture_output=True,
                check=True,
                text=True,
            )
            changed_files = {line.strip().replace("\\", "/") for line in proc.stdout.splitlines() if line.strip()}
        except Exception:
            changed_files = None  # Fallback to direct file inspection

    stale: List[Tuple[str, str, str]] = []

    for b in bindings:
        for owner in b.owners:
            norm_path = owner.path.replace("\\", "/")
            if changed_files is not None and norm_path not in changed_files:
                continue

            full_path = repo / owner.path
            if not full_path.is_file():
                stale.append((b.obligation_key, owner.path, "OWNER_FILE_MISSING"))
                continue

            res = compute_owner_digest(full_path, owner.symbol, owner.language, owner.path)
            if res.status != "found":
                stale.append((b.obligation_key, owner.path, f"OWNER_SYMBOL_{res.status.upper()}"))
            elif owner.owner_digest and res.digest != owner.owner_digest:
                stale.append((b.obligation_key, owner.path, "OWNER_DIGEST_CHANGED"))

    return stale
