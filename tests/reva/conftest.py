"""Pytest configuration and markers for REVA test suites."""

import pytest

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "reva_obligation(key): tag test with REVA obligation key")
    config.addinivalue_line("markers", "reva_case(kind): tag test with REVA case kind (positive, negative, boundary, malformed, journey)")
    config.addinivalue_line("markers", "reva_perf: performance budget test (reva-perf lane)")
    config.addinivalue_line("markers", "reva_fixtures: test runs against the deterministic REVA fixtures (reva-fixtures lane)")
    config.addinivalue_line("markers", "reva_depth(depth): tag test with REVA verification depth (static, unit, component, integration, acceptance, deployed, production_observed)")
