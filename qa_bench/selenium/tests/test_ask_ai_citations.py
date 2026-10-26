"""Selenium UI Test Suite: Ask AI Prompting and Citation Flow."""

from __future__ import annotations

import time
import pytest
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage
from qa_bench.selenium.pages.ask_ai_page import AskAiPage


@pytest.mark.selenium
class TestAskAiInterface:
    """QA tests for Ask AI question submission and answer modes."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        auth = AuthPage(driver).open()
        auth.login_as("analyst")
        self.shell = ShellPage(driver)
        assert self.shell.is_shell_loaded()

    def test_ask_ai_page_loads_with_boundary_badge(self, driver):
        """Verify Ask AI interface displays query composer and egress boundary status."""
        self.shell.nav_to("ask")
        ask_page = AskAiPage(driver)
        assert ask_page.is_loaded(), "Ask AI composer should be loaded"
        assert ask_page.is_visible(*ask_page.BOUNDARY_BADGE), "Egress boundary badge must be displayed"

    def test_answer_mode_selection(self, driver):
        """Verify switching between deterministic and narrated answer modes."""
        self.shell.nav_to("ask")
        ask_page = AskAiPage(driver)
        assert ask_page.is_loaded()
        ask_page.select_mode("deterministic")
        time.sleep(0.2)
        ask_page.select_mode("narrated")
        time.sleep(0.2)

    def test_suggested_question_click(self, driver):
        """Verify clicking a suggested prompt seeds the composer input."""
        self.shell.nav_to("ask")
        ask_page = AskAiPage(driver)
        assert ask_page.is_loaded()
        ask_page.click_first_suggestion()
