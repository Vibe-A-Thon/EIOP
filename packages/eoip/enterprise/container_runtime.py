"""Universal OCI container-runtime discovery and abstraction.

Probes the host for available container runtimes (Docker, Podman, nerdctl,
Finch, Lima, …) and exposes a normalized interface so callers never
hard-code a specific CLI.  The first healthy runtime wins, or the user
overrides with ``EOIP_CONTAINER_RUNTIME``.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import subprocess
from typing import Optional
from collections.abc import Sequence


@dataclasses.dataclass(frozen=True)
class ComposeInfo:
    command: tuple[str, ...]
    version: str


@dataclasses.dataclass(frozen=True)
class ContainerRuntime:
    name: str
    cli: str
    version: str
    compose: Optional[ComposeInfo]
    rootless: bool
    supports_init: bool
    supports_security_opt: bool
    supports_cap_drop: bool


_PROBE_ORDER: list[tuple[str, list[str]]] = [
    ("docker", ["docker"]),
    ("podman", ["podman"]),
    ("nerdctl", ["nerdctl"]),
    ("finch", ["finch"]),
    ("lima-nerdctl", ["lima", "nerdctl"]),
]

_COMPOSE_PROBES: list[tuple[str, list[list[str]]]] = [
    ("docker", [["docker", "compose"], ["docker-compose"]]),
    ("podman", [["podman", "compose"], ["podman-compose"]]),
    ("nerdctl", [["nerdctl", "compose"]]),
    ("finch", [["finch", "compose"]]),
    ("lima-nerdctl", [["lima", "nerdctl", "compose"]]),
]


def _run_quiet(args: Sequence[str], *, timeout: int = 10) -> Optional[str]:
    try:
        result = subprocess.run(
            list(args),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def _extract_version(raw: str) -> str:
    for token in raw.replace(",", " ").split():
        if any(ch.isdigit() for ch in token):
            return token.strip("v").split("-")[0]
    return raw.split("\n")[0][:60]


def _probe_runtime(name: str, cli_args: list[str]) -> Optional[tuple[str, str, str]]:
    cli_path = shutil.which(cli_args[0])
    if not cli_path:
        return None
    raw = _run_quiet([*cli_args, "version", "--format", "{{.Client.Version}}"])
    if not raw:
        raw = _run_quiet([*cli_args, "--version"])
    if not raw:
        return None
    return name, cli_args[0], _extract_version(raw)


def _probe_compose(runtime_name: str) -> Optional[ComposeInfo]:
    probes = dict(_COMPOSE_PROBES).get(runtime_name, [])
    for cmd_parts in probes:
        raw = _run_quiet([*cmd_parts, "version"])
        if raw:
            return ComposeInfo(
                command=tuple(cmd_parts),
                version=_extract_version(raw),
            )
    return None


def _detect_rootless(cli: str) -> bool:
    raw = _run_quiet([cli, "info", "--format", "json"])
    if not raw:
        raw = _run_quiet([cli, "info", "-f", "json"])
    if raw:
        try:
            info = json.loads(raw)
            sec = info.get("SecurityOptions") or info.get("security") or []
            if any("rootless" in str(s) for s in sec):
                return True
            if info.get("host", {}).get("security", {}).get("rootless"):
                return True
        except (json.JSONDecodeError, AttributeError):
            pass
    if cli in ("podman",):
        return os.getuid() != 0 if hasattr(os, "getuid") else True
    return False


def _runtime_capabilities(name: str) -> tuple[bool, bool, bool]:
    """(supports_init, supports_security_opt, supports_cap_drop) per runtime."""
    caps = {
        "docker": (True, True, True),
        "podman": (True, True, True),
        "nerdctl": (True, False, True),
        "finch": (True, False, True),
        "lima-nerdctl": (True, False, True),
    }
    return caps.get(name, (False, False, False))


def discover(*, preferred: Optional[str] = None) -> Optional[ContainerRuntime]:
    override = preferred or os.environ.get("EOIP_CONTAINER_RUNTIME")

    candidates = list(_PROBE_ORDER)
    if override:
        norm = override.lower().replace(" ", "-")
        candidates.sort(key=lambda x: 0 if x[0] == norm else 1)

    for name, cli_args in candidates:
        result = _probe_runtime(name, cli_args)
        if result is None:
            continue
        rt_name, cli, version = result
        compose = _probe_compose(rt_name)
        rootless = _detect_rootless(cli)
        init, secopt, capdrop = _runtime_capabilities(rt_name)
        return ContainerRuntime(
            name=rt_name,
            cli=cli,
            version=version,
            compose=compose,
            rootless=rootless,
            supports_init=init,
            supports_security_opt=secopt,
            supports_cap_drop=capdrop,
        )

    return None


def discover_all() -> list[ContainerRuntime]:
    """Return every detected runtime, ordered by probe priority."""
    found: list[ContainerRuntime] = []
    for name, cli_args in _PROBE_ORDER:
        result = _probe_runtime(name, cli_args)
        if result is None:
            continue
        rt_name, cli, version = result
        compose = _probe_compose(rt_name)
        rootless = _detect_rootless(cli)
        init, secopt, capdrop = _runtime_capabilities(rt_name)
        found.append(ContainerRuntime(
            name=rt_name,
            cli=cli,
            version=version,
            compose=compose,
            rootless=rootless,
            supports_init=init,
            supports_security_opt=secopt,
            supports_cap_drop=capdrop,
        ))
    return found


def require() -> ContainerRuntime:
    """Like :func:`discover` but raises if nothing is found."""
    rt = discover()
    if rt is None:
        raise EnvironmentError(
            "No OCI container runtime found. "
            "Install Docker, Podman, nerdctl, or Finch and ensure the CLI is on PATH. "
            "Override with EOIP_CONTAINER_RUNTIME=<name>."
        )
    return rt
