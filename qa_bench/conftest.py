"""Pytest fixtures and configuration for the KnowGridFlow QA Test Bench."""

from __future__ import annotations

import os
import sys
from contextlib import ExitStack
from pathlib import Path
import pytest
import httpx

from qa_bench.config import (
    REPO_ROOT,
    TEST_ROLES,
    BACKEND_URL,
    FRONTEND_URL,
    API_PREFIX,
    DEFAULT_BROWSER,
    HEADLESS_MODE,
    DEFAULT_TIMEOUT_SECS,
    SCREENSHOTS_DIR,
)

# Ensure repository root is on sys.path
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

pytest_plugins = ["eoip.verification.pytest_evidence"]


def pytest_configure(config):
    """Dynamically register custom markers to prevent strict-markers validation failures."""
    config.addinivalue_line("markers", "api: API contract and functional tests")
    config.addinivalue_line("markers", "selenium: Selenium browser automation tests")
    config.addinivalue_line("markers", "performance: latency and throughput benchmarks")
    config.addinivalue_line("markers", "e2e: end-to-end workflow scenario tests")
    config.addinivalue_line("markers", "security: security and DAST vulnerability tests")
    config.addinivalue_line("markers", "chaos: chaos and fault injection tests")


# ============================================================================
# API Test Fixtures (httpx)
# ============================================================================

@pytest.fixture
def inprocess_app(monkeypatch, tmp_path):
    """Create in-process FastAPI application instance for fast contract tests."""
    from apps.api.main import create_app
    from qa.runtime import environment

    for key, value in environment(tmp_path, {}).items():
        monkeypatch.setenv(key, value)
    keys = tmp_path / "qa-roles.keys"
    keys.write_text("\n".join(
        f"{entry.token} | {entry.role} | {entry.tenant} | {entry.username}"
        for entry in TEST_ROLES.values()
    ), encoding="utf-8")
    monkeypatch.setenv("EOIP_ASG_FILE", str(keys))
    return create_app()


@pytest.fixture
def api_client(inprocess_app):
    """Factory fixture returning an authenticated httpx.Client for a given role."""
    from fastapi.testclient import TestClient

    clients = ExitStack()

    def _make_client(role_name: str = "superadmin", use_remote: bool = False) -> httpx.Client | TestClient:
        role = TEST_ROLES[role_name.lower()]
        headers = {
            "Authorization": f"Bearer {role.token}",
            "X-Tenant-Id": role.tenant,
            "Accept": "application/json",
        }
        if use_remote:
            if os.environ.get("QA_ALLOW_REMOTE") != "true" or not os.environ.get(f"QA_TOKEN_{role_name.upper()}"):
                raise RuntimeError("Remote QA requires QA_ALLOW_REMOTE=true and an explicit role token")
            return clients.enter_context(httpx.Client(
                base_url=f"{BACKEND_URL}{API_PREFIX}",
                headers=headers,
                timeout=DEFAULT_TIMEOUT_SECS,
                trust_env=False,
            ))
        # Use TestClient with /api/v1 base prefix
        tc = clients.enter_context(TestClient(inprocess_app, base_url="http://testserver/api/v1"))
        tc.headers.update(headers)
        return tc

    yield _make_client
    clients.close()


@pytest.fixture
def superadmin_client(api_client):
    return api_client("superadmin")


@pytest.fixture
def admin_client(api_client):
    return api_client("admin")


@pytest.fixture
def steward_client(api_client):
    return api_client("steward")


@pytest.fixture
def analyst_client(api_client):
    return api_client("analyst")


@pytest.fixture
def viewer_client(api_client):
    return api_client("viewer")


@pytest.fixture
def unauthenticated_client(inprocess_app):
    from fastapi.testclient import TestClient
    with TestClient(inprocess_app, base_url="http://testserver/api/v1") as client:
        yield client


# ============================================================================
# Selenium WebDriver Fixtures
# ============================================================================

def _build_chrome_driver(headless: bool = True):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    # Enable browser console logging for audit
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return webdriver.Chrome(options=options)


def _build_edge_driver(headless: bool = True):
    from selenium import webdriver
    from selenium.webdriver.edge.options import Options as EdgeOptions
    options = EdgeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Edge(options=options)


@pytest.fixture
def driver(request):
    """Selenium WebDriver fixture with automatic screenshot capture on test failure."""
    browser_type = getattr(request, "param", DEFAULT_BROWSER)
    driver_instance = None
    try:
        if browser_type == "edge":
            driver_instance = _build_edge_driver(headless=HEADLESS_MODE)
        else:
            driver_instance = _build_chrome_driver(headless=HEADLESS_MODE)
        driver_instance.implicitly_wait(2.0)
        driver_instance.set_page_load_timeout(DEFAULT_TIMEOUT_SECS)
    except Exception as exc:
        pytest.skip(f"Could not initialize Selenium driver for {browser_type}: {exc}")

    yield driver_instance

    # Capture failure screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name.replace("[", "_").replace("]", "_")
        screenshot_path = SCREENSHOTS_DIR / f"fail_{test_name}.png"
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        try:
            driver_instance.save_screenshot(str(screenshot_path))
            print(f"\n[Selenium QA] Screenshot saved to: {screenshot_path}")
        except Exception:
            pass

    if driver_instance:
        driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
