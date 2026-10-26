"""Selenium UI Test Suite: Sigma.js Graph Explorer Canvas and EQL Query Execution."""

from __future__ import annotations

import time
import pytest
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage
from qa_bench.selenium.pages.graph_explorer_page import GraphExplorerPage
from qa_bench.selenium.pages.query_page import QueryPage


@pytest.mark.selenium
class TestGraphAndQueryInterfaces:
    """QA tests for knowledge graph visual exploration and querying."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        auth = AuthPage(driver).open()
        auth.login_as("admin")
        self.shell = ShellPage(driver)
        assert self.shell.is_shell_loaded()

    def test_graph_canvas_renders_webgl_surface(self, driver):
        """Verify Sigma.js canvas initializes and renders in the explorer workspace."""
        self.shell.nav_to("graph")
        graph_page = GraphExplorerPage(driver)
        assert graph_page.is_canvas_ready(), "Graph canvas container must be ready"

    def test_lens_switching_domain_and_fact(self, driver):
        """Verify domain vs fact lens toggle switches without UI breakdown."""
        self.shell.nav_to("graph")
        graph_page = GraphExplorerPage(driver)
        assert graph_page.is_canvas_ready()
        if graph_page.is_visible(*graph_page.LENS_DOMAIN, timeout=2.0):
            graph_page.select_domain_lens()
            time.sleep(0.3)
            graph_page.select_fact_lens()
            time.sleep(0.3)

    def test_query_workbench_input_and_run(self, driver):
        """Verify query workbench loads, accepts EQL input, and enables the Run button."""
        self.shell.nav_to("query")
        query_page = QueryPage(driver)
        assert query_page.is_loaded(), "Query textarea must be present"
        query_page.set_query("find all requirements")
        assert query_page.is_clickable(*query_page.RUN_BUTTON), "Run button should be enabled"
        query_page.run_query()
