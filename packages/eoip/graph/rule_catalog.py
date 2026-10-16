"""Architecture rule catalog (G2-ARCHC-002): stored, named rule sets.

Rule sets are DSL files loaded from two locations:

- ``config/architecture/*.rules`` — shipped defaults (versioned with the repo)
- ``<EOIP_DATA_DIR>/state/arch-rules/*.rules`` — operator-managed overrides

``POST /api/v1/conformance/check`` can reference a named rule set so callers
do not have to resend rule text on every call.
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_RULES_DIR = Path("config/architecture")


def _state_rules_dir() -> Path:
    return Path(os.environ.get("EOIP_DATA_DIR", ".data")) / "state" / "arch-rules"


def list_rule_sets() -> list[dict]:
    """List available rule sets (name, origin, path, rule count)."""
    from eoip.graph.conformance import parse_rules

    sets = []
    for origin, directory in (("default", DEFAULT_RULES_DIR), ("custom", _state_rules_dir())):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.rules")):
            text = path.read_text(encoding="utf-8")
            sets.append(
                {
                    "name": path.stem,
                    "origin": origin,
                    "path": str(path),
                    "rule_count": len(parse_rules(text)),
                }
            )
    return sets


def get_rule_set(name: str) -> str | None:
    """Return the DSL text for a rule set, custom overrides first."""
    for directory in (_state_rules_dir(), DEFAULT_RULES_DIR):
        path = directory / f"{name}.rules"
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return None


def save_rule_set(name: str, dsl_text: str) -> Path:
    """Persist an operator rule set; validates the DSL first."""
    from eoip.graph.conformance import parse_rules

    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError("rule set name must be alphanumeric")
    rules = parse_rules(dsl_text)
    if not rules:
        raise ValueError("rule set contains no valid RULE declarations")
    directory = _state_rules_dir()
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"{name}.rules"
    destination.write_text(dsl_text, encoding="utf-8")
    return destination
