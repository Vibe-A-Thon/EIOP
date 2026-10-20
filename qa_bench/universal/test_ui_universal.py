"""Universal Selenium UI coverage: every screen x every role x every control.

Routes are parsed from ``frontend/src/App.tsx`` at collection time, so a newly
added screen is covered automatically. For each screen this suite:

  1. renders it (as every RBAC persona) and asserts the shell survives with no
     uncaught JS exceptions and no unexpected 404;
  2. crawls every visible control inside ``<main>`` -- buttons, tabs, switches,
     checkboxes, selects, text inputs -- clicking/typing each one and asserting
     the app never crashes (no error boundary exists, so a crash blanks the shell);
  3. types an XSS canary into every text field and asserts it never executes.

Destructive controls (delete, sign out, purge, ...) are skipped by label.
A JSON interaction ledger is written to ``qa_bench/reports/ui_interaction_ledger.json``.
"""

from __future__ import annotations

import json
import time

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from qa_bench.config import HEADLESS_MODE, REPORTS_DIR, TEST_ROLES
from qa_bench.selenium.pages.auth_page import AuthPage
from qa_bench.selenium.pages.shell_page import ShellPage
from qa_bench.universal.route_inventory import concrete_ui_path, discover_frontend_routes

ROUTES = discover_frontend_routes()
ROUTE_IDS = [p.strip("/").replace("/", "_").replace(":", "") or "root" for p, _ in ROUTES]
ROLES = [r for r in TEST_ROLES if r != "bootstrap"]

DESTRUCTIVE = (
    "delete", "remove", "purge", "drop", "revoke", "sign out", "signout", "log out",
    "logout", "reset", "destroy", "wipe", "erase", "terminate", "disable tenant", "rotate",
)
XSS_CANARY = '<img src=x onerror="window.__qa_xss=1">'
MAX_CONTROLS_PER_SCREEN = 60
LEDGER: dict[str, dict] = {}


# --------------------------------------------------------------------------
# Fixtures: one browser per role per module keeps the run tractable.
# --------------------------------------------------------------------------

def _make_driver():
    from qa_bench.conftest import _build_chrome_driver

    try:
        d = _build_chrome_driver(headless=HEADLESS_MODE)
    except Exception as exc:  # pragma: no cover - environment dependent
        pytest.skip(f"Chrome WebDriver unavailable: {exc}")
    d.implicitly_wait(0.5)
    return d


def _login(driver, role: str) -> ShellPage:
    AuthPage(driver).login_as(role)
    shell = ShellPage(driver)
    assert shell.is_shell_loaded(), f"Shell failed to load after sign-in as {role}"
    driver.get_log("browser")  # drain sign-in noise
    return shell


@pytest.fixture(scope="module")
def superadmin_session():
    d = _make_driver()
    try:
        _login(d, "superadmin")
        yield d
    finally:
        d.quit()
        out = REPORTS_DIR / "ui_interaction_ledger.json"
        out.write_text(json.dumps(LEDGER, indent=2), encoding="utf-8")


@pytest.fixture(scope="module", params=ROLES)
def role_session(request):
    d = _make_driver()
    try:
        _login(d, request.param)
        yield request.param, d
    finally:
        d.quit()


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def spa_navigate(driver, path: str) -> None:
    """Client-side navigation (auth lives in React memory; a reload would log out)."""
    driver.execute_script(
        "window.history.pushState({}, '', arguments[0]);"
        "window.dispatchEvent(new PopStateEvent('popstate', {state: {}}));",
        path,
    )
    time.sleep(0.6)  # framer-motion route transition


def uncaught_errors(driver) -> list[str]:
    try:
        logs = driver.get_log("browser")
    except WebDriverException:
        return []
    return [
        l["message"] for l in logs
        if l.get("level") == "SEVERE" and ("Uncaught" in l["message"] or "TypeError" in l["message"]
                                           or "ReferenceError" in l["message"])
    ]


def shell_alive(driver) -> bool:
    return bool(driver.find_elements(By.CSS_SELECTOR, '[data-testid="app-shell-nav-rail"]')) and bool(
        driver.find_elements(By.TAG_NAME, "main")
    )


def assert_screen_healthy(driver, path: str, expect_404: bool, context: str) -> None:
    assert shell_alive(driver), f"[{context}] App crashed (shell unmounted) on {path}"
    main = driver.find_element(By.TAG_NAME, "main")
    assert main.text.strip() or main.find_elements(By.CSS_SELECTOR, "canvas,svg"), \
        f"[{context}] {path} rendered an empty <main>"
    is_404 = bool(driver.find_elements(By.CSS_SELECTOR, '[data-testid="not-found"]'))
    assert is_404 == expect_404, f"[{context}] {path}: not-found shown={is_404}, expected={expect_404}"
    errs = uncaught_errors(driver)
    assert not errs, f"[{context}] Uncaught JS errors on {path}: {errs[:3]}"


def _label(el) -> str:
    try:
        return " ".join(filter(None, [
            el.text, el.get_attribute("aria-label"), el.get_attribute("title"),
            el.get_attribute("data-testid"), el.get_attribute("name"), el.get_attribute("placeholder"),
        ])).strip()[:80]
    except WebDriverException:
        return ""


CONTROL_SELECTOR = (
    "main button, main [role='tab'], main [role='switch'], main [role='button'], "
    "main input[type='checkbox'], main input[type='radio'], main select, "
    "main input:not([type]), main input[type='text'], main input[type='search'], main textarea"
)


def collect_controls(driver) -> list[tuple[str, str, str]]:
    """Return a stable list of (selector-index-key, tag, label) for visible enabled controls."""
    found = []
    for idx, el in enumerate(driver.find_elements(By.CSS_SELECTOR, CONTROL_SELECTOR)):
        try:
            if not el.is_displayed() or not el.is_enabled():
                continue
            found.append((str(idx), el.tag_name, _label(el)))
        except WebDriverException:
            continue
    return found[:MAX_CONTROLS_PER_SCREEN]


def exercise(driver, index: int, tag: str, label: str) -> str:
    els = driver.find_elements(By.CSS_SELECTOR, CONTROL_SELECTOR)
    if index >= len(els):
        return "vanished"
    el = els[index]
    if any(word in label.lower() for word in DESTRUCTIVE):
        return "skipped-destructive"
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        input_type = (el.get_attribute("type") or "").lower()
        if tag == "select":
            sel = Select(el)
            if len(sel.options) > 1:
                sel.select_by_index(len(sel.options) - 1)
            return "selected"
        if tag == "textarea" or (tag == "input" and input_type in ("", "text", "search")):
            el.clear()
            el.send_keys(XSS_CANARY)
            return "typed"
        driver.execute_script("arguments[0].click();", el)
        return "clicked"
    except WebDriverException as exc:
        return f"error:{type(exc).__name__}"


def close_overlays(driver) -> None:
    from selenium.webdriver.common.keys import Keys
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except WebDriverException:
        pass


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

@pytest.mark.selenium
@pytest.mark.universal
def test_route_inventory_is_complete():
    """Every screen component file must be wired to a route (no orphaned screens)."""
    from qa_bench.universal.route_inventory import screen_files

    routed = {c for _, c in ROUTES} | {"SignIn"}
    orphans = [s for s in screen_files() if s not in routed]
    assert not orphans, f"Screen components with no route (untestable/unreachable): {orphans}"
    assert len(ROUTES) >= 25, f"Route discovery looks broken: {ROUTES}"


@pytest.mark.selenium
@pytest.mark.universal
@pytest.mark.parametrize("path,component", ROUTES, ids=ROUTE_IDS)
def test_every_screen_renders(superadmin_session, path, component):
    driver = superadmin_session
    target = concrete_ui_path(path)
    spa_navigate(driver, target)
    assert_screen_healthy(driver, target, expect_404=(path == "*"), context=f"render:{component}")


@pytest.mark.selenium
@pytest.mark.universal
@pytest.mark.parametrize("path,component", ROUTES, ids=ROUTE_IDS)
def test_every_control_on_every_screen(superadmin_session, path, component):
    """Click/type/select every visible control; the app must never crash or execute injected script."""
    driver = superadmin_session
    target = concrete_ui_path(path)
    spa_navigate(driver, target)
    if not shell_alive(driver):
        pytest.fail(f"{target} crashed before interaction")

    controls = collect_controls(driver)
    actions = []
    for key, tag, label in controls:
        if driver.current_url.split("?")[0].rstrip("/").endswith(target.rstrip("/")) is False:
            spa_navigate(driver, target)  # a control navigated away; come back
        outcome = exercise(driver, int(key), tag, label)
        time.sleep(0.15)
        actions.append({"control": label or tag, "tag": tag, "outcome": outcome})
        assert shell_alive(driver), f"Interacting with '{label or tag}' on {target} crashed the app"
        errs = uncaught_errors(driver)
        assert not errs, f"'{label or tag}' on {target} raised uncaught JS errors: {errs[:3]}"
        close_overlays(driver)

    xss = driver.execute_script("return window.__qa_xss === 1")
    LEDGER[target] = {"component": component, "controls_found": len(controls), "actions": actions}
    assert not xss, f"XSS canary executed on {target} -- unsanitised HTML rendering"


@pytest.mark.selenium
@pytest.mark.universal
@pytest.mark.rbac
@pytest.mark.parametrize("path,component", ROUTES, ids=ROUTE_IDS)
def test_every_screen_for_every_role(role_session, path, component):
    """Each persona sees every screen render (content or a graceful denial) -- never a crash."""
    role, driver = role_session
    target = concrete_ui_path(path)
    spa_navigate(driver, target)
    assert_screen_healthy(driver, target, expect_404=(path == "*"), context=f"{role}:{component}")


@pytest.mark.selenium
@pytest.mark.universal
def test_every_nav_rail_link_resolves(superadmin_session):
    """Every NavRail entry must land on a real screen (never the 404 page)."""
    driver = superadmin_session
    spa_navigate(driver, "/overview")
    links = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="app-shell-nav-"]')
    ids = [l.get_attribute("data-testid") for l in links if l.get_attribute("data-testid") != "app-shell-nav-rail"]
    assert ids, "NavRail exposes no navigation items"
    broken = []
    for testid in ids:
        el = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="{testid}"]')
        if not el or not el[0].is_displayed():
            continue
        driver.execute_script("arguments[0].click();", el[0])
        time.sleep(0.5)
        if driver.find_elements(By.CSS_SELECTOR, '[data-testid="not-found"]') or not shell_alive(driver):
            broken.append(testid)
    assert not broken, f"NavRail links that lead to 404/crash: {broken}"


@pytest.mark.selenium
@pytest.mark.universal
def test_unauthenticated_deep_links_redirect_to_signin():
    """Every protected route must bounce an anonymous user to /signin."""
    from qa_bench.config import FRONTEND_URL

    d = _make_driver()
    try:
        leaks = []
        for path, _ in ROUTES:
            d.get(f"{FRONTEND_URL}{concrete_ui_path(path)}")
            time.sleep(0.4)
            if "/signin" not in d.current_url:
                leaks.append(path)
        assert not leaks, f"Protected routes reachable without sign-in: {leaks}"
    finally:
        d.quit()
