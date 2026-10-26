"""Selenium UI Test Suite: Theme Switching and Visual Density Verification."""

from __future__ import annotations

import time
import pytest
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage


@pytest.mark.selenium
class TestThemeAndVisualSystem:
    """QA Automation suite for Swiss Workbench token and theme controls."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        auth = AuthPage(driver).open()
        auth.login_as("admin")
        self.shell = ShellPage(driver)
        assert self.shell.is_shell_loaded()

    @pytest.mark.parametrize("theme_id", ["dark", "light", "hc-dark", "hc-light"])
    def test_theme_toggle_updates_html_data_theme(self, driver, theme_id):
        """Verify theme switcher updates the root data-theme attribute cleanly."""
        self.shell.set_theme(theme_id)
        current_theme = self.shell.get_theme()
        assert current_theme == theme_id, f"Expected data-theme='{theme_id}', got '{current_theme}'"
