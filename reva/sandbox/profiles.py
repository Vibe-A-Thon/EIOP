"""Execution profiles for verifier sandbox (T-204 / REVA-VS-001 / §6.7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

from reva.core.errors import RevaValidationError
from reva.kernel.authority import Depth
from reva.sandbox.limits import SandboxLimits


@dataclass
class ProfileSpec:
    """Execution profile defining engine, network policy, and resource caps."""

    name: str
    depth: Depth
    engine: Literal["process", "container", "compose"]
    network: Literal["none", "loopback", "compose"]
    limits: SandboxLimits = field(default_factory=SandboxLimits)
    container_image: Optional[str] = None


PROFILES: Dict[str, ProfileSpec] = {
    "static": ProfileSpec(
        name="static",
        depth=Depth.STATIC,
        engine="process",
        network="none",
        limits=SandboxLimits(cpu_seconds=120, wall_timeout_s=300),
    ),
    "unit": ProfileSpec(
        name="unit",
        depth=Depth.UNIT,
        engine="process",
        network="none",
        limits=SandboxLimits(cpu_seconds=300, wall_timeout_s=600),
    ),
    "component": ProfileSpec(
        name="component",
        depth=Depth.COMPONENT,
        engine="process",
        network="loopback",
        limits=SandboxLimits(cpu_seconds=600, wall_timeout_s=900),
    ),
    "integration": ProfileSpec(
        name="integration",
        depth=Depth.INTEGRATION,
        engine="process",
        network="loopback",
        limits=SandboxLimits(cpu_seconds=900, wall_timeout_s=1800),
        container_image="reva-verifier-python:latest",
    ),
    "acceptance": ProfileSpec(
        name="acceptance",
        depth=Depth.ACCEPTANCE,
        engine="compose",
        network="compose",
        limits=SandboxLimits(cpu_seconds=1800, wall_timeout_s=3600),
        container_image="reva-verifier-e2e:latest",
    ),
    "re_disasm": ProfileSpec(
        name="re_disasm",
        depth=Depth.COMPONENT,
        engine="container",
        network="none",
        limits=SandboxLimits(cpu_seconds=600, wall_timeout_s=900, address_space_bytes=4 * 1024 * 1024 * 1024),
        container_image="reva-re-disasm:latest",
    ),
    "re_ghidra": ProfileSpec(
        name="re_ghidra",
        depth=Depth.INTEGRATION,
        engine="container",
        network="none",
        limits=SandboxLimits(cpu_seconds=900, wall_timeout_s=1200, address_space_bytes=8 * 1024 * 1024 * 1024),
        container_image="reva-re-ghidra:latest",
    ),
    "re_dynamic_tracing": ProfileSpec(
        name="re_dynamic_tracing",
        depth=Depth.COMPONENT,
        engine="container",
        network="none",
        limits=SandboxLimits(cpu_seconds=300, wall_timeout_s=600, address_space_bytes=2 * 1024 * 1024 * 1024),
        container_image="reva-re-trace:latest",
    ),
    "re_browser_cdp": ProfileSpec(
        name="re_browser_cdp",
        depth=Depth.ACCEPTANCE,
        engine="container",
        network="loopback",
        limits=SandboxLimits(cpu_seconds=180, wall_timeout_s=300, address_space_bytes=2 * 1024 * 1024 * 1024),
        container_image="reva-re-browser:latest",
    ),
}


def get_profile(name: str) -> ProfileSpec:
    """Retrieve profile by name or raise RevaValidationError."""
    if name not in PROFILES:
        raise RevaValidationError(f"Unknown sandbox profile '{name}', expected one of {list(PROFILES.keys())}")
    return PROFILES[name]
