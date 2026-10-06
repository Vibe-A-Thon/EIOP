"""Health / support bundle collector (requirements §47 / GAP-OPS-003).

Gathers redacted configuration, recent audit events, graph statistics, and
runtime versions into a single JSON-serialisable bundle suitable for support
handoff. All config values pass through ``eoip.audit.redaction`` so secrets
never leave the system.
"""

from __future__ import annotations

import os
import platform
import time
from collections.abc import Iterable
from typing import Any

from eoip.audit.redaction import redact_secrets

_BUNDLE_SCHEMA = "urn:eoip:ops:support-bundle:v1"


_SENSITIVE_ENV_PARTS = ("TOKEN", "SECRET", "PASSWORD", "PASS", "KEY", "CREDENTIAL")


def _redact_env(name: str, value):
    if value is None:
        return None
    if any(part in name.upper() for part in _SENSITIVE_ENV_PARTS):
        return "***REDACTED***"
    return value


def _versions() -> dict[str, str]:
    versions = {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    try:
        from importlib.metadata import version

        versions["eoip"] = version("eoip")
    except Exception:  # noqa: BLE001 — package metadata is optional
        versions["eoip"] = "unknown"
    return versions


def _graph_stats(graph_store: Any) -> dict[str, Any]:
    if graph_store is None:
        return {"available": False}
    stats: dict[str, Any] = {"available": True}
    try:
        ping = graph_store.ping() if hasattr(graph_store, "ping") else None
        if ping:
            stats["ping"] = ping
        stats["healthy"] = graph_store.health() if hasattr(graph_store, "health") else True
    except Exception as exc:  # noqa: BLE001
        stats["error"] = str(exc)
    return stats


def _recent_audit(audit_sink: Any, limit: int) -> list[dict]:
    if audit_sink is None:
        return []
    try:
        events = audit_sink.read(limit=limit) if hasattr(audit_sink, "read") else []
    except Exception as exc:  # noqa: BLE001
        return [{"error": str(exc)}]
    return [redact_secrets(event) if isinstance(event, dict) else {"event": str(event)} for event in events]


def collect_support_bundle(
    *,
    audit_sink: Any = None,
    graph_store: Any = None,
    env_vars: Iterable[str] = (
        "EOIP_GRAPH_BACKEND",
        "EOIP_GRAPH_CONFIG",
        "EOIP_GRAPH_URL",
        "EOIP_HUGEGRAPH_URL",
        "EOIP_API_TOKEN",
        "EOIP_ENV",
    ),
    max_audit_events: int = 50,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Collect a single redacted support bundle document (§47).

    - config: the requested environment variables, redacted via
      ``eoip.audit.redaction.redact_secrets``;
    - audit_events: the most recent events from ``audit_sink.read``;
    - graph_stats: health/ping output from the graph store;
    - versions: Python, platform, and eoip package versions.
    """
    config = redact_secrets({name: _redact_env(name, os.getenv(name)) for name in env_vars})
    bundle: dict[str, Any] = {
        "id": f"urn:eoip:ops:support-bundle:{int(time.time())}",
        "schema": _BUNDLE_SCHEMA,
        "config": config,
        "audit_events": _recent_audit(audit_sink, max_audit_events),
        "graph_stats": _graph_stats(graph_store),
        "versions": _versions(),
    }
    if extra:
        bundle["extra"] = redact_secrets(extra)
    return bundle
