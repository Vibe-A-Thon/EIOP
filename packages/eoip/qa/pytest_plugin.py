"""Pytest plugin for behavioral-evidence collection (SR-QA-010).

Enable with ``-p eoip.qa.pytest_plugin`` (or via ``pytest_plugins`` in a
conftest).  The plugin registers the ``eoip_requirement`` marker and, after
each test, records explicitly declared requirement IDs — from markers and
from :func:`eoip.qa.evidence.record_requirement` calls — into a
:class:`~eoip.qa.evidence.RunCollector`.

Critically (lesson from ``eoip.gaps.coverage``'s literal string matcher):
this plugin NEVER inspects docstrings, comments or source text.  Only the
marker and the explicit runtime call count.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from eoip.qa.evidence import COLLECTOR_ENV_VAR, RunCollector, drain_recorded_requirements

MARKER_NAME = "eoip_requirement"

_collector = RunCollector()


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        f"{MARKER_NAME}(req_id): declare that this test provides behavioral "
        "evidence for requirement req_id (SR-QA-010; explicit declarations "
        "only — docstring references never count).",
    )


def pytest_runtest_setup(item):
    drain_recorded_requirements()  # drop leakage from previous tests


def pytest_runtest_teardown(item, nextitem):
    marker_ids: list[str] = []
    for mark in item.iter_markers(name=MARKER_NAME):
        for arg in mark.args:
            if isinstance(arg, str):
                marker_ids.append(arg)
        if isinstance(mark.kwargs.get("ids"), (list, tuple)):
            marker_ids.extend(str(i) for i in mark.kwargs["ids"])
    call_ids = drain_recorded_requirements()
    if marker_ids or call_ids:
        _collector.record_test(
            test_id=item.nodeid,
            marker_ids=marker_ids,
            call_ids=call_ids,
            recorded_at=datetime.now(UTC).isoformat(),
        )


def pytest_sessionfinish(session, exitstatus):
    out = os.environ.get(COLLECTOR_ENV_VAR)
    if out:
        _collector.write(out)


def get_collector() -> RunCollector:
    """Return the module-level collector (useful for in-process assertions)."""
    return _collector
