"""Resource limits and enforcement for verifier sandbox (T-203 / REVA-VS-003)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SandboxLimits:
    """Resource constraints for sandbox processes."""

    cpu_seconds: int = 900
    address_space_bytes: int = 4 * 1024 * 1024 * 1024  # 4 GiB
    file_size_bytes: int = 1 * 1024 * 1024 * 1024  # 1 GiB
    max_open_files: int = 4096
    max_processes: int = 512
    wall_timeout_s: int = 1800
    stdout_cap_bytes: int = 16 * 1024 * 1024  # 16 MiB
    stderr_cap_bytes: int = 16 * 1024 * 1024  # 16 MiB


def apply_rlimits(limits: SandboxLimits) -> None:
    """Apply resource limits in subprocess preexec_fn on platforms that support it."""
    try:
        import resource

        # RLIMIT_CPU
        resource.setrlimit(resource.RLIMIT_CPU, (limits.cpu_seconds, limits.cpu_seconds))
        # RLIMIT_AS
        if hasattr(resource, "RLIMIT_AS"):
            resource.setrlimit(resource.RLIMIT_AS, (limits.address_space_bytes, limits.address_space_bytes))
        # RLIMIT_FSIZE
        resource.setrlimit(resource.RLIMIT_FSIZE, (limits.file_size_bytes, limits.file_size_bytes))
        # RLIMIT_NOFILE
        resource.setrlimit(resource.RLIMIT_NOFILE, (limits.max_open_files, limits.max_open_files))
        # RLIMIT_NPROC
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(resource.RLIMIT_NPROC, (limits.max_processes, limits.max_processes))
        # RLIMIT_CORE = 0
        if hasattr(resource, "RLIMIT_CORE"):
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, AttributeError, ValueError, OSError):
        # Platform does not support resource module (e.g. Windows) or permission issue
        pass
