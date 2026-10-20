"""Explicit, reviewable test quarantine for CI (FT-F04).

Set ``EOIP_TEST_QUARANTINE_FILE`` to a file of pytest node ids, one per line, each
followed by ``#`` and the tracking id/reason. Listed tests are deselected (not
skipped, not xfailed) and printed in the terminal summary, so CI stays meaningful
for everything else without hiding which tests are known-red. Without the
variable the plugin does nothing, so local runs still execute every test.

Only tests whose fix needs an owner decision belong here; each line must carry
a reason.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

ENV_VAR = "EOIP_TEST_QUARANTINE_FILE"
_KEY = pytest.StashKey[list[tuple[str, str]]]()


def load_quarantine(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        node_id, sep, reason = line.partition("#")
        node_id, reason = node_id.strip(), reason.strip()
        if not sep or not reason:
            raise pytest.UsageError(f"{path}:{number}: quarantine entry needs '# <tracking id> <reason>'")
        entries[node_id] = reason
    return entries


def _match(node_id: str, entries: dict[str, str]) -> str | None:
    if node_id in entries:
        return entries[node_id]
    base = node_id.split("[", 1)[0]
    return entries.get(base)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    path = os.environ.get(ENV_VAR)
    if not path:
        return
    entries = load_quarantine(Path(path))
    keep: list[pytest.Item] = []
    dropped: list[pytest.Item] = []
    reasons: list[tuple[str, str]] = []
    for item in items:
        reason = _match(item.nodeid, entries)
        if reason is None:
            keep.append(item)
        else:
            dropped.append(item)
            reasons.append((item.nodeid, reason))
    if dropped:
        config.hook.pytest_deselected(items=dropped)
        items[:] = keep
    config.stash[_KEY] = reasons


def pytest_terminal_summary(terminalreporter, exitstatus: int, config: pytest.Config) -> None:
    reasons = config.stash.get(_KEY, [])
    if not reasons:
        return
    terminalreporter.section(f"quarantined tests ({len(reasons)}, deselected via {ENV_VAR})")
    for node_id, reason in reasons:
        terminalreporter.write_line(f"{node_id}  # {reason}")
