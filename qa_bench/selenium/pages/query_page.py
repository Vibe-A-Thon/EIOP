"""Query Workbench Page Object representing /query."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.base_page import BasePage


class QueryPage(BasePage):
    """Page object for EQL / SPARQL query sandbox."""

    PATH = "/query"

    QUERY_TEXTAREA = (By.CSS_SELECTOR, '[data-testid="query-input"]')
    RUN_BUTTON = (By.CSS_SELECTOR, '[data-testid="query-run"]')
    SAMPLE_CHIPS = (By.CSS_SELECTOR, "button.rounded-full")

    def open(self) -> QueryPage:
        self.navigate_to(self.PATH)
        self.wait_for_page_ready()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(*self.QUERY_TEXTAREA, timeout=8.0)

    def set_query(self, query_text: str) -> None:
        self.type_text(*self.QUERY_TEXTAREA, query_text)

    def run_query(self) -> None:
        self.click(*self.RUN_BUTTON)
