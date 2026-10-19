"""
Repository URL Ingestion & Ephemeral Cloner (REVA-AB-014, T-ENH-001).
Safely clones public/private git repositories from GitHub, GitLab, Bitbucket,
and generic Git servers into an isolated, ephemeral sandbox root.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from reva.core.errors import RevaError

class RepositoryClonerError(RevaError):
    """Raised when repository cloning or validation fails."""


@dataclass(frozen=True)
class ClonedRepository:
    """Metadata representing a safely cloned or ingested repository."""
    repo_id: str
    clone_path: str
    commit_sha: str
    remote_url: str
    branch: str
    file_count: int
    total_bytes: int
    is_ephemeral: bool = True


class GitRepositoryCloner:
    """
    Safely clones remote repositories into an ephemeral temporary root,
    applying strict depth limits, timeouts, and quota enforcement.
    """

    ALLOWED_SCHEMES = ("https://", "http://", "git://", "ssh://", "git@", "file://")
    DANGEROUS_CHARS = re.compile(r"[;&|`$><!]")

    def __init__(
        self,
        base_scratch_dir: Optional[str] = None,
        max_size_bytes: int = 5 * 1024 * 1024 * 1024, # 5 GiB
        timeout_seconds: int = 300,
        default_depth: int = 1,
    ) -> None:
        self.base_scratch_dir = base_scratch_dir or tempfile.gettempdir()
        self.max_size_bytes = max_size_bytes
        self.timeout_seconds = timeout_seconds
        self.default_depth = default_depth

    def validate_url(self, url: str) -> None:
        """Validates that URL is well-formed and contains no shell injection vectors."""
        if not url or not isinstance(url, str):
            raise RepositoryClonerError("Repository URL must be a non-empty string.")

        clean_url = url.strip()
        if self.DANGEROUS_CHARS.search(clean_url):
            raise RepositoryClonerError(f"Security error: dangerous characters detected in URL: {clean_url}")

        if not any(clean_url.startswith(scheme) for scheme in self.ALLOWED_SCHEMES):
            raise RepositoryClonerError(f"Unsupported repository URL protocol: {clean_url}")

    def clone(self, repo_url: str, branch: Optional[str] = None, depth: Optional[int] = None) -> ClonedRepository:
        """
        Executes sandboxed shallow git clone into a unique ephemeral directory.
        """
        self.validate_url(repo_url)
        depth = depth or self.default_depth

        # Generate unique temp directory
        target_dir = tempfile.mkdtemp(prefix="reva_repo_", dir=self.base_scratch_dir)

        # Build git clone command
        cmd = ["git", "clone", "--depth", str(depth)]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([repo_url.strip(), target_dir])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            if result.returncode != 0:
                raise RepositoryClonerError(f"Git clone failed: {result.stderr.strip() or result.stdout.strip()}")

            # Determine commit SHA
            rev_res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            commit_sha = rev_res.stdout.strip()

            # Determine current branch
            br_res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            active_branch = br_res.stdout.strip()

            # Audit file counts and size quota
            file_count = 0
            total_bytes = 0
            for root, _, files in os.walk(target_dir):
                for f in files:
                    file_count += 1
                    fp = os.path.join(root, f)
                    total_bytes += os.path.getsize(fp)
                    if total_bytes > self.max_size_bytes:
                        raise RepositoryClonerError(f"Repository exceeds maximum allowed size quota of {self.max_size_bytes} bytes.")

            # Compute stable repo_id from URL
            repo_id = re.sub(r"[^a-zA-Z0-9_-]", "_", repo_url.split("/")[-1].replace(".git", ""))

            return ClonedRepository(
                repo_id=repo_id,
                clone_path=target_dir,
                commit_sha=commit_sha,
                remote_url=repo_url,
                branch=active_branch,
                file_count=file_count,
                total_bytes=total_bytes,
                is_ephemeral=True,
            )
        except Exception as e:
            # Clean up on failure
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir, ignore_errors=True)
            if isinstance(e, RepositoryClonerError):
                raise
            raise RepositoryClonerError(f"Clone operation error: {str(e)}") from e

    def ingest(self, repo_source: str, branch: Optional[str] = None, depth: Optional[int] = None) -> ClonedRepository:
        """
        Unified repository ingestion: accepts remote URLs (GitHub, GitLab, Bitbucket)
        or local repository filesystem paths.
        """
        clean_source = repo_source.strip()
        # If it's an existing directory on the filesystem
        if os.path.isdir(clean_source):
            abs_path = os.path.abspath(clean_source)
            commit_sha = "unknown"
            active_branch = "main"

            # Check if it has a git directory
            if os.path.isdir(os.path.join(abs_path, ".git")):
                try:
                    rev_res = subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        cwd=abs_path,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    commit_sha = rev_res.stdout.strip()
                    br_res = subprocess.run(
                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        cwd=abs_path,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    active_branch = br_res.stdout.strip()
                except Exception:
                    pass

            file_count = 0
            total_bytes = 0
            for root, dirs, files in os.walk(abs_path):
                # skip .git and node_modules
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__")]
                for f in files:
                    file_count += 1
                    fp = os.path.join(root, f)
                    try:
                        total_bytes += os.path.getsize(fp)
                    except OSError:
                        pass

            repo_id = re.sub(r"[^a-zA-Z0-9_-]", "_", os.path.basename(abs_path))
            return ClonedRepository(
                repo_id=repo_id,
                clone_path=abs_path,
                commit_sha=commit_sha,
                remote_url=abs_path,
                branch=active_branch,
                file_count=file_count,
                total_bytes=total_bytes,
                is_ephemeral=False,
            )

        # Otherwise clone as remote repository
        return self.clone(repo_url=clean_source, branch=branch, depth=depth)

    def cleanup(self, cloned_repo: ClonedRepository) -> None:
        """Removes the ephemeral clone directory if it was temporarily cloned."""
        if cloned_repo and cloned_repo.is_ephemeral and os.path.exists(cloned_repo.clone_path):
            shutil.rmtree(cloned_repo.clone_path, ignore_errors=True)
