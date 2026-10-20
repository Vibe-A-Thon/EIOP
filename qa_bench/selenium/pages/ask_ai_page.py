"""Ask AI Page Object representing /ask."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.base_page import BasePage


class AskAiPage(BasePage):
    """Page object for Ask AI query interface."""

    PATH = "/ask"

    QUERY_INPUT = (By.CSS_SELECTOR, '[data-testid="ask-query-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="ask-submit-button"]')
    MODE_DETERMINISTIC = (By.CSS_SELECTOR, '[data-testid="ask-mode-deterministic"]')
    MODE_NARRATED = (By.CSS_SELECTOR, '[data-testid="ask-mode-narrated"]')
    BOUNDARY_BADGE = (By.CSS_SELECTOR, '[data-testid="ask-boundary-badge"]')
    SUGGESTION_FIRST = (By.CSS_SELECTOR, '[data-testid="ask-suggestion-0"]')

    def open(self) -> AskAiPage:
        self.navigate_to(self.PATH)
        self.wait_for_page_ready()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(*self.QUERY_INPUT, timeout=8.0)

    def select_mode(self, mode: str = "deterministic") -> None:
        if mode == "deterministic":
            self.click(*self.MODE_DETERMINISTIC)
        else:
            self.click(*self.MODE_NARRATED)

    def ask(self, question: str) -> None:
        self.type_text(*self.QUERY_INPUT, question)
        self.click(*self.SUBMIT_BUTTON)

    def click_first_suggestion(self) -> None:
        if self.is_visible(*self.SUGGESTION_FIRST, timeout=3.0):
            self.click(*self.SUGGESTION_FIRST)
