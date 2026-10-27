"""Deterministic, file-level test sharding for parallel CI jobs.

Set ``EOIP_TEST_SHARD=i/n`` (1-based) to keep only the test files assigned to shard ``i`` of
``n``; the rest are deselected (reported, never skipped). Without the variable the plugin does
nothing, so local runs and the single-coordinator evidence receipts are unchanged. Each shard is
an ordinary single-process pytest run, so ``--run-evidence`` stays valid per shard.

Assignment is per test file, so module/class fixtures never straddle shards. Files are packed by
longest-processing-time first using ``EOIP_TEST_SHARD_WEIGHTS`` (JSON ``{"tests/x.py": seconds}``,
regenerate with ``scripts/ci/update_shard_weights.py``); files missing from it get the median
weight. The result depends only on the collected file set and the weights, so every shard of the
same commit computes the same partition. ``EOIP_TEST_SHARD_MANIFEST`` writes what this shard
collected and kept; ``scripts/ci/check_test_shards.py`` proves the shards partition the suite
(nothing lost, nothing run twice).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from statistics import median

import pytest

SHARD_VAR = "EOIP_TEST_SHARD"
WEIGHTS_VAR = "EOIP_TEST_SHARD_WEIGHTS"
MANIFEST_VAR = "EOIP_TEST_SHARD_MANIFEST"
_EMPTY = pytest.StashKey[bool]()
_SETTINGS = pytest.StashKey[tuple[int, int, "str | None", "str | None"]]()


def parse_shard(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", value)
    if not match:
        raise pytest.UsageError(f"{SHARD_VAR}={value!r}: expected 'i/n', e.g. '2/4'")
    index, total = int(match.group(1)), int(match.group(2))
    if total < 1 or not 1 <= index <= total:
        raise pytest.UsageError(f"{SHARD_VAR}={value!r}: need 1 <= i <= n")
    return index, total


def load_weights(path: str | None) -> dict[str, float]:
    if not path:
        return {}
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise pytest.UsageError(f"{WEIGHTS_VAR}={path!r}: unreadable ({type(exc).__name__})") from exc
    if not isinstance(raw, dict):
        raise pytest.UsageError(f"{WEIGHTS_VAR}={path!r}: expected a JSON object of file -> seconds")
    return {str(k): float(v) for k, v in raw.items() if isinstance(v, (int, float)) and v >= 0}


def assign_files(files: list[str], total: int, weights: dict[str, float]) -> dict[str, int]:
    """Map each file to a 1-based shard: heaviest first onto the least-loaded shard."""
    unique = set(files)
    known = [weights[f] for f in unique if f in weights]
    default = median(known) if known else 1.0
    order = sorted(unique, key=lambda f: (-weights.get(f, default), f))
    loads = [0.0] * total
    assignment: dict[str, int] = {}
    for name in order:
        slot = min(range(total), key=lambda s: (loads[s], s))
        loads[slot] += max(weights.get(name, default), 0.001)
        assignment[name] = slot + 1
    return assignment


def _file_of(item: pytest.Item) -> str:
    return item.nodeid.split("::", 1)[0]


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    # Read once and remove from the environment: tests that start a child pytest must run their
    # inner suite whole, not silently sharded (or overwrite this shard's manifest).
    settings = {name: os.environ.pop(name, None) for name in (SHARD_VAR, WEIGHTS_VAR, MANIFEST_VAR)}
    if settings[SHARD_VAR]:
        config.stash[_SETTINGS] = (*parse_shard(settings[SHARD_VAR]), settings[WEIGHTS_VAR], settings[MANIFEST_VAR])


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    settings = config.stash.get(_SETTINGS, None)
    if settings is None:
        return
    index, total, weights, manifest = settings
    collected = [item.nodeid for item in items]
    assignment = assign_files([_file_of(item) for item in items], total, load_weights(weights))
    keep = [item for item in items if assignment[_file_of(item)] == index]
    drop = [item for item in items if assignment[_file_of(item)] != index]
    if drop:
        config.hook.pytest_deselected(items=drop)
        items[:] = keep
    config.stash[_EMPTY] = bool(collected) and not keep
    if manifest:
        path = Path(manifest)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "schema_version": "eoip-test-shard-v1", "shard": index, "total": total,
            "collected": sorted(collected), "assigned": sorted(item.nodeid for item in keep),
            "files": {name: slot for name, slot in sorted(assignment.items()) if slot == index},
        }, indent=1), encoding="utf-8")


def pytest_report_header(config: pytest.Config) -> str | None:
    settings = config.stash.get(_SETTINGS, None)
    return f"test shard {settings[0]}/{settings[1]} (by file; {SHARD_VAR})" if settings else None


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    # A shard that legitimately received no files is not "no tests collected" for the suite;
    # the partition check still proves the other shards covered everything.
    if session.config.stash.get(_EMPTY, False) and int(exitstatus) == int(pytest.ExitCode.NO_TESTS_COLLECTED):
        session.exitstatus = pytest.ExitCode.OK
