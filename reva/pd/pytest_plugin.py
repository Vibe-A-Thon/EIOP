"""Pytest plugin for REVA Proof-of-Done metadata collection (T-206 / AG-02 / AG-06)."""

from __future__ import annotations

import unittest.mock
import pytest

_ORIGINAL_PATCH_ENTER = unittest.mock._patch.__enter__


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "reva_obligation(key): link test to REVA obligation key")
    config.addinivalue_line("markers", "reva_case(kind): define REVA test case kind")


def pytest_runtest_setup(item):
    """Record REVA user properties on each test item."""
    item.user_properties.append(("reva_nodeid", item.nodeid))

    # Collect reva_obligation markers
    for mark in item.iter_markers(name="reva_obligation"):
        for arg in mark.args:
            item.user_properties.append(("reva_obligation", str(arg)))

    # Collect reva_case markers
    for mark in item.iter_markers(name="reva_case"):
        for arg in mark.args:
            item.user_properties.append(("reva_case", str(arg)))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Monitor unittest.mock.patch calls during test execution for AG-06 anti-gaming."""
    patched_targets = []

    def _hooked_enter(self):
        target = getattr(self, "target", None)
        attribute = getattr(self, "attribute", None)
        getter = getattr(self, "getter", None)
        name = ""
        if hasattr(target, "__name__"):
            name = target.__name__
        elif target is not None:
            name = str(target)
        if attribute:
            name = f"{name}.{attribute}" if name else attribute
        if getter:
            try:
                name = str(getter())
            except Exception:
                pass
        if name:
            patched_targets.append(name)
        return _ORIGINAL_PATCH_ENTER(self)

    unittest.mock._patch.__enter__ = _hooked_enter
    try:
        yield
    finally:
        unittest.mock._patch.__enter__ = _ORIGINAL_PATCH_ENTER
        if patched_targets:
            item.user_properties.append(("reva_patched", ",".join(patched_targets)))
