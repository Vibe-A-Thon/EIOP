"""Shared test bootstrap for subprocess-based CLI tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "packages"

for path in (REPO_ROOT, PACKAGE_ROOT):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

existing = [part for part in os.environ.get("PYTHONPATH", "").split(os.pathsep) if part]
desired = [str(REPO_ROOT), str(PACKAGE_ROOT)]
os.environ["PYTHONPATH"] = os.pathsep.join(desired + [part for part in existing if part not in desired])

# ---------------------------------------------------------------------------
# BASE-02: Collect @pytest.mark.req requirement IDs and emit test map
# ---------------------------------------------------------------------------
import json

_COLLECTED_REQ_MAP: dict[str, set[str]] = {}


def pytest_collection_modifyitems(session, config, items):
    """Scan collected test items for requirement marks."""
    global _COLLECTED_REQ_MAP
    _COLLECTED_REQ_MAP = {}
    for item in items:
        # Collect from @pytest.mark.req(...)
        for mark in item.iter_markers(name="req"):
            for arg in mark.args:
                if isinstance(arg, str) and arg.strip():
                    _COLLECTED_REQ_MAP.setdefault(arg.strip(), set()).add(item.nodeid)
                elif isinstance(arg, (list, tuple)):
                    for sub in arg:
                        if isinstance(sub, str) and sub.strip():
                            _COLLECTED_REQ_MAP.setdefault(sub.strip(), set()).add(item.nodeid)

        # Collect from @pytest.mark.eoip_requirement(...)
        for mark in item.iter_markers(name="eoip_requirement"):
            for arg in mark.args:
                if isinstance(arg, str) and arg.strip():
                    _COLLECTED_REQ_MAP.setdefault(arg.strip(), set()).add(item.nodeid)


def pytest_sessionfinish(session, exitstatus):
    """Emit or update requirements-test-map.json at repository root."""
    if not _COLLECTED_REQ_MAP:
        return

    out_file = REPO_ROOT / "requirements-test-map.json"
    current_map: dict[str, list[str]] = {}
    if out_file.exists():
        try:
            raw = json.loads(out_file.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                current_map = {k: list(v) if isinstance(v, list) else [v] for k, v in raw.items()}
        except Exception:
            current_map = {}

    for req_id, nodeids in _COLLECTED_REQ_MAP.items():
        existing_nodes = set(current_map.get(req_id, []))
        existing_nodes.update(nodeids)
        current_map[req_id] = sorted(existing_nodes)

    try:
        out_file.write_text(json.dumps(dict(sorted(current_map.items())), indent=2), encoding="utf-8")
    except Exception:
        pass

