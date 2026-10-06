"""Preflight checks (requirements §47 / GAP-OPS-001).

Validates that a node is fit to run before traffic is admitted:
required environment variables, ontology YAML parseability, graph store
reachability, API token configuration, disk-space headroom, and port
availability. Checks never raise — every check reports pass/warn/fail so a
report can be surfaced by the API layer.
"""

from __future__ import annotations

import os
import shutil
import socket
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_REQUIRED_ENV: tuple[str, ...] = ()
DEFAULT_TOKEN_ENV = "EOIP_API_TOKEN"
DEFAULT_MIN_FREE_BYTES = 1 * 1024**3  # 1 GiB warning threshold


@dataclass
class CheckResult:
    """One preflight check outcome."""

    name: str
    status: str  # "pass" | "warn" | "fail"
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.status != "fail"


@dataclass
class PreflightReport:
    """Aggregate preflight outcome (§47)."""

    checks: list[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks)

    @property
    def failures(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "fail"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "warn"]

    def to_dict(self) -> dict:
        return {
            "id": "urn:eoip:ops:preflight-report:current",
            "ok": self.ok,
            "checks": [
                {"name": c.name, "status": c.status, "detail": c.detail}
                for c in self.checks
            ],
        }


def _check_env(required: Iterable[str]) -> CheckResult:
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        return CheckResult("env", "fail", f"missing required env vars: {', '.join(missing)}")
    return CheckResult("env", "pass", f"{len(list(required))} required env var(s) present")


def _check_token(token_env: str) -> CheckResult:
    if os.getenv(token_env):
        return CheckResult("token", "pass", f"{token_env} is configured")
    return CheckResult("token", "warn", f"{token_env} is not set; auth endpoints will be disabled")


def _check_ontology(paths: Iterable[Path]) -> CheckResult:
    paths = list(paths)
    if not paths:
        return CheckResult("ontology", "warn", "no ontology YAML files provided to validate")
    bad: list[str] = []
    for path in paths:
        try:
            yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 — report, never raise
            bad.append(f"{path}: {exc}")
    if bad:
        return CheckResult("ontology", "fail", "; ".join(bad))
    return CheckResult("ontology", "pass", f"{len(paths)} ontology YAML file(s) parseable")


def _check_graph_store(store: Any) -> CheckResult:
    if store is None:
        return CheckResult("graph_store", "warn", "no graph store provided; reachability not verified")
    try:
        healthy = store.health() if hasattr(store, "health") else bool(store.ping())
    except Exception as exc:  # noqa: BLE001
        return CheckResult("graph_store", "fail", f"unreachable: {exc}")
    if healthy:
        return CheckResult("graph_store", "pass", "graph store reachable")
    return CheckResult("graph_store", "fail", "graph store reported unhealthy")


def _check_disk(min_free_bytes: int, path: str | Path) -> CheckResult:
    usage = shutil.disk_usage(path)
    if usage.free < min_free_bytes:
        return CheckResult(
            "disk_space", "warn",
            f"only {usage.free / 1024**2:.0f} MiB free on {path} (threshold {min_free_bytes / 1024**3:.1f} GiB)",
        )
    return CheckResult("disk_space", "pass", f"{usage.free / 1024**3:.2f} GiB free on {path}")


def _check_port(port: int, host: str) -> CheckResult:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError as exc:
            return CheckResult("port", "fail", f"{host}:{port} unavailable: {exc}")
    return CheckResult("port", "pass", f"{host}:{port} is available")


def run_preflight(
    *,
    required_env: Iterable[str] = DEFAULT_REQUIRED_ENV,
    ontology_paths: Iterable[str | Path] = (),
    graph_store: Any = None,
    token_env: str = DEFAULT_TOKEN_ENV,
    min_free_bytes: int = DEFAULT_MIN_FREE_BYTES,
    disk_path: str | Path = ".",
    port: int | None = None,
    host: str = "0.0.0.0",
) -> PreflightReport:
    """Run all preflight checks and return an aggregate report (§47)."""
    required = list(required_env)
    report = PreflightReport()
    report.checks.append(_check_env(required))
    report.checks.append(_check_token(token_env))
    report.checks.append(_check_ontology([Path(p) for p in ontology_paths]))
    report.checks.append(_check_graph_store(graph_store))
    report.checks.append(_check_disk(min_free_bytes, disk_path))
    if port is not None:
        report.checks.append(_check_port(port, host))
    return report
