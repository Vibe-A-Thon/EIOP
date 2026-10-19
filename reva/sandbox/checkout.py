"""Clean checkout and ephemeral git worktree management (T-205 / REVA-VS-002 / AG-09)."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from reva.core.errors import RevaDirtyTreeError, RevaIntegrityError


def compute_tree_digest(worktree_path: Path) -> str:
    """Compute deterministic SHA-256 digest of sorted git ls-files -s."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(worktree_path), "ls-files", "-s"],
            capture_output=True,
            check=True,
            text=True,
        )
        lines = sorted([l.strip() for l in proc.stdout.splitlines() if l.strip()])
        payload = "\n".join(lines).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
    except subprocess.SubprocessError as e:
        raise RevaIntegrityError(f"Failed to compute git tree digest: {e}") from e


@dataclass
class Worktree:
    """Clean checkout working tree."""

    repo_path: Path
    worktree_path: Path
    commit: str
    tree_digest: str
    is_ephemeral: bool = True

    def cleanup(self) -> None:
        """Remove ephemeral worktree."""
        if not self.is_ephemeral:
            return
        try:
            subprocess.run(
                ["git", "-C", str(self.repo_path), "worktree", "remove", "--force", str(self.worktree_path)],
                capture_output=True,
                check=False,
            )
            if self.worktree_path.exists():
                shutil.rmtree(self.worktree_path, ignore_errors=True)
        except Exception:
            pass

    def __enter__(self) -> Worktree:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cleanup()


def prepare_worktree(
    repo_path: Union[str, Path],
    commit: str,
    dest_dir: Optional[Union[str, Path]] = None,
    allow_dirty_parent: bool = False,
) -> Worktree:
    """Create a clean, isolated git worktree at the specified commit."""
    repo = Path(repo_path).resolve()

    # Check for uncommitted changes in parent if not allowed
    if not allow_dirty_parent:
        try:
            status = subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain"],
                capture_output=True,
                check=True,
                text=True,
            )
            # If porcelain output is non-empty, parent repo is dirty
            if status.stdout.strip():
                raise RevaDirtyTreeError("Working tree contains uncommitted changes; clean commit required")
        except subprocess.SubprocessError as e:
            if not isinstance(e, RevaDirtyTreeError):
                pass

    if dest_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="reva_wt_")
        wt_path = Path(temp_dir)
    else:
        wt_path = Path(dest_dir).resolve()
        wt_path.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["git", "-C", str(repo), "worktree", "add", "--detach", str(wt_path), commit],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RevaIntegrityError(f"Failed to add git worktree at {commit}: {e.stderr.decode('utf-8', errors='replace')}") from e

    # Verify worktree itself is pristine
    status_wt = subprocess.run(
        ["git", "-C", str(wt_path), "status", "--porcelain"],
        capture_output=True,
        check=True,
        text=True,
    )
    if status_wt.stdout.strip():
        raise RevaDirtyTreeError(f"New worktree at {commit} is unexpectedly dirty")

    tree_digest = compute_tree_digest(wt_path)
    return Worktree(
        repo_path=repo,
        worktree_path=wt_path,
        commit=commit,
        tree_digest=tree_digest,
        is_ephemeral=True,
    )
