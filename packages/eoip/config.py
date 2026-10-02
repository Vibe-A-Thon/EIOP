"""YAML config loading for policies and agents."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from eoip.query.policy import QueryPolicy


def _config_root() -> Path:
    return Path(os.getenv("EOIP_CONFIG_DIR", "config"))


def load_query_policy(name: str = "default") -> QueryPolicy:
    path = _config_root() / "query-policies" / f"{name}.yaml"
    if not path.exists():
        return QueryPolicy()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return QueryPolicy(
        max_depth=data.get("max_depth", 8),
        max_results=data.get("max_results", 500),
        max_timeout_ms=data.get("max_timeout_ms", 30000),
        allowed_intents=frozenset(data.get("allowed_intents", [])),
        blocked_edges=frozenset(data.get("blocked_edges", [])),
        read_only=data.get("read_only", True),
    )


def load_agent_config(agent_id: str) -> dict | None:
    path = _config_root() / "agents" / f"{agent_id.lower().replace(' ', '-')}.yaml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))
