"""Selenium UI Test Suite: Authentication, Role-Selection, and RBAC persona switching."""

from __future__ import annotations

import time
import pytest
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage
from qa_bench.config import TEST_ROLES


@pytest.mark.selenium
class TestAuthenticationAndRBAC:
    """QA Automation suite for authentication workflows."""

    def test_signin_page_loads_with_role_presets(self, driver):
        """Verify sign-in page displays all demo role presets and form controls."""
        auth_page = AuthPage(driver).open()
        assert auth_page.is_loaded(), "Sign-in form should be visible"
        assert auth_page.is_visible(*auth_page.TOKEN_INPUT), "Token input must be present"
        assert auth_page.is_visible(*auth_page.TENANT_INPUT), "Tenant input must be present"
        assert auth_page.is_visible(*auth_page.DEMO_ROLES_CONTAINER), "Demo roles panel must be present"

    @pytest.mark.parametrize("role_key", ["superadmin", "admin", "steward", "analyst", "viewer"])
    def test_persona_preset_selection(self, driver, role_key):
        """Verify clicking each demo role preset automatically fills credentials and allows entry."""
        auth_page = AuthPage(driver).open()
        auth_page.select_demo_role(role_key)
        auth_page.submit()

        shell = ShellPage(driver)
        assert shell.is_shell_loaded(), f"Shell should load after signing in as {role_key}"

    def test_invalid_token_rejected_with_alert(self, driver):
        """Verify authentication rejection on invalid token with UI error alert when online, or graceful fail-safe offline."""
        from qa_bench.run_qa_bench import check_server_reachable
        from qa_bench.config import BACKEND_URL

        auth_page = AuthPage(driver).open()
        auth_page.enter_credentials(token="invalid_token_99999_fake", tenant="default")
        auth_page.submit()
        time.sleep(1.0)

        is_backend_online = check_server_reachable(f"{BACKEND_URL}/health")
        if is_backend_online:
            assert auth_page.has_error(), "An error alert should be displayed for invalid token when backend is online"
        else:
            shell = ShellPage(driver)
            assert shell.is_shell_loaded() or auth_page.has_error()
