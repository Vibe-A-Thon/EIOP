"""Base Page Object Model providing resilient waits and cross-cutting helpers."""

from __future__ import annotations

import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from qa_bench.config import FRONTEND_URL, DEFAULT_TIMEOUT_SECS


class BasePage:
    """Base class for all KnowGridFlow Page Objects."""

    def __init__(self, driver: webdriver.Chrome | webdriver.Edge, timeout: float = DEFAULT_TIMEOUT_SECS):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to(self, path: str = "/") -> None:
        """Navigate to relative or absolute path."""
        url = path if path.startswith("http") else f"{FRONTEND_URL}{path}"
        self.driver.get(url)

    def find(self, by: By, value: str, timeout: float | None = None) -> WebElement:
        """Find an element with explicit wait."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located((by, value)),
            message=f"Element not present: ({by}, {value})",
        )

    def find_visible(self, by: By, value: str, timeout: float | None = None) -> WebElement:
        """Find a visible element with explicit wait."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located((by, value)),
            message=f"Element not visible: ({by}, {value})",
        )

    def find_clickable(self, by: By, value: str, timeout: float | None = None) -> WebElement:
        """Find an element ready to be clicked."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable((by, value)),
            message=f"Element not clickable: ({by}, {value})",
        )

    def find_all(self, by: By, value: str) -> List[WebElement]:
        """Find all matching elements."""
        return self.driver.find_elements(by, value)

    def find_by_testid(self, testid: str, timeout: float | None = None) -> WebElement:
        """Convenience selector for data-testid."""
        return self.find_visible(By.CSS_SELECTOR, f'[data-testid="{testid}"]', timeout=timeout)

    def click(self, by: By, value: str) -> None:
        """Scroll into view and click element."""
        el = self.find_clickable(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        el.click()

    def js_click(self, by: By, value: str) -> None:
        """Click element via JavaScript to bypass overlay and sticky-header intercepts."""
        el = self.find(by, value)
        self.driver.execute_script("arguments[0].click();", el)

    def click_testid(self, testid: str) -> None:
        """Click element by data-testid."""
        self.click(By.CSS_SELECTOR, f'[data-testid="{testid}"]')

    def type_text(self, by: By, value: str, text: str, clear: bool = True) -> None:
        """Type text into an input field."""
        el = self.find_visible(by, value)
        if clear:
            el.clear()
        el.send_keys(text)

    def get_text(self, by: By, value: str) -> str:
        """Get text content of an element."""
        return self.find_visible(by, value).text.strip()

    def is_present(self, by: By, value: str, timeout: float = 2.0) -> bool:
        """Check if element is present in DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def is_visible(self, by: By, value: str, timeout: float = 2.0) -> bool:
        """Check if element is visible on page."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, by: By, value: str, timeout: float = 2.0) -> bool:
        """Check if element is clickable on page."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
            return True
        except TimeoutException:
            return False

    def get_theme(self) -> str:
        """Get current HTML [data-theme] attribute."""
        html = self.driver.find_element(By.TAG_NAME, "html")
        return html.get_attribute("data-theme") or "dark"

    def get_browser_console_errors(self) -> List[dict]:
        """Retrieve browser console error logs."""
        try:
            logs = self.driver.get_log("browser")
            return [l for l in logs if l.get("level") in ("SEVERE", "ERROR")]
        except Exception:
            return []

    def wait_for_page_ready(self, timeout: float = 10.0) -> None:
        """Wait until document.readyState == 'complete'."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
