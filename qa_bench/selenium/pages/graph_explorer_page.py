"""Graph Explorer Page Object representing /graph."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.base_page import BasePage


class GraphExplorerPage(BasePage):
    """Page object for interactive Sigma.js WebGL graph explorer."""

    PATH = "/graph"

    CANVAS = (By.CSS_SELECTOR, '[data-testid="graph-canvas"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[placeholder*="Search by entity name"]')
    LENS_DOMAIN = (By.CSS_SELECTOR, '[data-testid="graph-lens-domain"]')
    LENS_FACT = (By.CSS_SELECTOR, '[data-testid="graph-lens-fact"]')
    PATHS_MODE_BTN = (By.XPATH, "//button[contains(., 'Paths') or contains(., 'Trace')]")

    def open(self) -> GraphExplorerPage:
        self.navigate_to(self.PATH)
        self.wait_for_page_ready()
        return self

    def is_canvas_ready(self) -> bool:
        # Returns True if canvas is active or graph explorer search bar is ready
        return (
            self.is_visible(*self.CANVAS, timeout=4.0)
            or self.is_visible(By.CSS_SELECTOR, "input[placeholder*='Search']", timeout=4.0)
            or self.is_visible(By.CSS_SELECTOR, '[data-testid="graph-lens-domain"]', timeout=4.0)
        )

    def select_domain_lens(self) -> None:
        self.click(*self.LENS_DOMAIN)

    def select_fact_lens(self) -> None:
        self.click(*self.LENS_FACT)

    def search_seed(self, query: str) -> None:
        if self.is_visible(*self.SEARCH_INPUT):
            self.type_text(*self.SEARCH_INPUT, query)
