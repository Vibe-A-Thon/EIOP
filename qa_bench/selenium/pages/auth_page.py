"""Authentication Page Object representing /signin."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from qa_bench.selenium.pages.base_page import BasePage
from qa_bench.config import TEST_ROLES


class AuthPage(BasePage):
    """Page object for KnowGridFlow sign-in screen."""

    PATH = "/signin"

    # Selectors
    FORM = (By.CSS_SELECTOR, '[data-testid="signin-form"]')
    TOKEN_INPUT = (By.CSS_SELECTOR, '[data-testid="signin-token-input"]')
    TENANT_INPUT = (By.CSS_SELECTOR, '[data-testid="signin-tenant-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="signin-submit-button"]')
    ERROR_ALERT = (By.CSS_SELECTOR, '[data-testid="signin-error"]')
    DEMO_ROLES_CONTAINER = (By.CSS_SELECTOR, '[data-testid="signin-demo-roles"]')

    def open(self) -> AuthPage:
        self.navigate_to(self.PATH)
        self.wait_for_page_ready()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(*self.FORM, timeout=5.0)

    def select_demo_role(self, role_key: str) -> AuthPage:
        """Click one of the pre-configured role buttons."""
        key_formatted = role_key.lower().replace(" ", "-").replace("_", "-")
        if key_formatted == "superadmin":
            key_formatted = "super-admin"
        btn_selector = (By.CSS_SELECTOR, f'[data-testid="signin-role-{key_formatted}"]')
        self.click(*btn_selector)
        return self

    def enter_credentials(self, token: str, tenant: str = "default") -> AuthPage:
        self.type_text(*self.TOKEN_INPUT, token)
        self.type_text(*self.TENANT_INPUT, tenant)
        return self

    def submit(self) -> None:
        self.click(*self.SUBMIT_BUTTON)

    def login_as(self, role_name: str = "superadmin") -> None:
        """Full login flow for a given role name."""
        self.open()
        role = TEST_ROLES.get(role_name.lower())
        if not role:
            raise ValueError(f"Unknown test role: {role_name}")
        self.select_demo_role(role_name)
        if role.tenant != "*":
            self.type_text(*self.TENANT_INPUT, role.tenant)
        self.submit()

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_ALERT)

    def has_error(self) -> bool:
        return self.is_visible(*self.ERROR_ALERT, timeout=2.0)
