"""AppShell Page Object representing navigation, top bar, and theme controls."""

from __future__ import annotations

import time
from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.base_page import BasePage


class ShellPage(BasePage):
    """Page object for global shell, rail navigation, and top bar."""

    NAV_RAIL = (By.CSS_SELECTOR, '[data-testid="app-shell-nav-rail"]')
    THEME_BUTTON = (By.CSS_SELECTOR, '[data-testid="theme-toggle-button"]')
    BACKEND_CHIP = (By.CSS_SELECTOR, '[data-testid="backend-status-chip"]')
    TENANT_DROPDOWN = (By.CSS_SELECTOR, '[data-testid="tenant-select-dropdown"]')
    SEARCH_TRIGGER = (By.CSS_SELECTOR, '[data-testid="global-search-trigger"]')

    def is_shell_loaded(self) -> bool:
        return self.is_visible(*self.NAV_RAIL, timeout=8.0)

    def nav_to(self, item_id: str) -> None:
        """Navigate to workspace screen by item ID (e.g. 'overview', 'graph', 'ask', 'query')."""
        selector = (By.CSS_SELECTOR, f'[data-testid="app-shell-nav-{item_id}"]')
        self.click(*selector)
        self.wait_for_page_ready()

    def set_theme(self, theme_name: str) -> None:
        """Switch theme using the top-bar theme dropdown."""
        self.js_click(*self.THEME_BUTTON)
        time.sleep(0.3)
        option_selector = (By.CSS_SELECTOR, f'[data-testid="theme-option-{theme_name}"]')
        self.js_click(*option_selector)
        time.sleep(0.3)  # Allow CSS transition

    def get_backend_status_text(self) -> str:
        if self.is_visible(*self.BACKEND_CHIP, timeout=3.0):
            return self.get_text(*self.BACKEND_CHIP)
        return ""

    def get_tenant_workspace_text(self) -> str:
        return self.get_text(*self.TENANT_DROPDOWN)
