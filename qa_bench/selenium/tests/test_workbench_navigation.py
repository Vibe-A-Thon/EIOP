"""Selenium UI Test Suite: Full 22+ Screen Navigation and Rendering Audit."""

from __future__ import annotations

import time
import pytest
from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage


# All primary task screens in the KnowGridFlow Emergent workbench
TASK_SCREENS = [
    ("overview", "/overview", "Overview"),
    ("ask", "/ask", "Ask"),
    ("graph", "/graph", "Graph Explorer"),
    ("meta-graph", "/meta-graph", "Meta-graph"),
    ("query", "/query", "Query"),
    ("impact", "/impact", "Impact"),
    ("changes", "/changes", "Changes"),
    ("time", "/time", "Time Travel"),
    ("incidents", "/incidents", "Incidents"),
    ("ontology", "/ontology", "Ontology"),
    ("quality", "/quality", "Quality"),
    ("snapshots", "/snapshots", "Snapshots"),
    ("ingestion", "/ingestion", "Ingestion"),
    ("agents", "/agents", "Agents"),
    ("reports", "/reports", "Reports"),
    ("collaboration", "/collaboration", "Collaboration"),
    ("health", "/health", "Health"),
    ("governance", "/governance", "Governance"),
    ("brand", "/brand", "Brand"),
    ("tenant", "/tenant", "Tenant"),
    ("settings", "/settings", "Settings"),
    ("help", "/help", "Help"),
]


@pytest.mark.selenium
class TestWorkbenchNavigationAudit:
    """Comprehensive screen-by-screen audit of the entire workbench UI."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        """Sign in as admin before navigating screens."""
        auth = AuthPage(driver).open()
        auth.login_as("admin")
        shell = ShellPage(driver)
        assert shell.is_shell_loaded(), "Shell must be loaded before running navigation tests"
        self.shell = shell

    @pytest.mark.parametrize("screen_id,route,label", TASK_SCREENS)
    def test_screen_renders_without_fatal_exceptions(self, driver, screen_id, route, label):
        """Navigate to each screen, ensure page loads, and verify no SEVERE JS console errors."""
        # Navigate via NavRail or direct route
        self.shell.nav_to(screen_id)
        time.sleep(0.4)  # Allow page transition animation

        # Verify page rendered content inside main element
        main_content = driver.find_element(By.TAG_NAME, "main")
        assert main_content.is_displayed(), f"Main content container should be displayed for {route}"

        # Assert no uncaught JS runtime errors
        console_errors = self.shell.get_browser_console_errors()
        fatal_errors = [e["message"] for e in console_errors if "Uncaught" in e.get("message", "")]
        assert len(fatal_errors) == 0, f"Uncaught JavaScript exceptions detected on {route}: {fatal_errors}"
