"""Regression test for CC3-019: REVA import collision and namespace resolution.

The proxy package ``packages/reva/__init__.py`` (which exposed no ``config``)
collided with the real root ``reva/`` package: whichever ``sys.path`` order a
preceding test left behind decided which one ``import reva`` resolved to, so
``tests/security/test_route_role_policy.py`` passed alone but failed in a full
run. The proxy is removed; these tests pin the resolution and the imports the
security suite performs.
"""

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PACKAGES_DIR = REPO_ROOT / "packages"
EXPECTED_ROOT_REVA = (REPO_ROOT / "reva" / "__init__.py").resolve()


def _pollute_sys_path_with_packages_first():
    """Reproduce the preceding-test pollution: 'packages' ahead of the repo root."""
    for path in (str(REPO_ROOT), str(PACKAGES_DIR)):
        if path in sys.path:
            sys.path.remove(path)
    sys.path.insert(0, str(REPO_ROOT))
    sys.path.insert(0, str(PACKAGES_DIR))
    for name in [m for m in sys.modules if m == "reva" or m.startswith("reva.")]:
        del sys.modules[name]


def test_reva_proxy_package_is_not_reintroduced():
    # packages/reva must never again shadow the root reva package.
    assert not (PACKAGES_DIR / "reva" / "__init__.py").exists(), (
        "packages/reva/__init__.py is the removed CC3-019 proxy; do not reintroduce it"
    )


def test_reva_resolves_to_root_package_and_has_config():
    # Even if 'packages' is prepended to sys.path, 'reva' must resolve to root 'reva/'
    _pollute_sys_path_with_packages_first()

    import reva
    actual_reva_file = Path(reva.__file__).resolve()

    assert actual_reva_file == EXPECTED_ROOT_REVA, (
        f"reva.__file__ ({actual_reva_file}) must match root {EXPECTED_ROOT_REVA}"
    )

    from reva import config
    assert hasattr(config, "RevaSettings")
    assert hasattr(config, "get_settings")


def test_security_suite_reva_imports_resolve_after_path_pollution():
    """Mirror test_route_role_policy.py's imports after a polluting preceding test."""
    _pollute_sys_path_with_packages_first()

    reva = importlib.import_module("reva")
    assert Path(reva.__file__).resolve() == EXPECTED_ROOT_REVA

    reva_config = importlib.import_module("reva.config")  # the import that failed under the proxy
    assert hasattr(reva_config, "RevaSettings") and hasattr(reva_config, "set_settings")
    gaps = importlib.import_module("reva.api.routes_gaps")
    assert hasattr(gaps, "record_gap")
    importlib.import_module("apps.api.main")  # imported by the security test before reva

    # Re-importing after apps.api.main must still resolve to the root package.
    reva_again = importlib.import_module("reva")
    assert Path(reva_again.__file__).resolve() == EXPECTED_ROOT_REVA
