"""Regression test for CC3-019: REVA import collision and namespace resolution."""

import sys
from pathlib import Path


def test_reva_resolves_to_root_package_and_has_config():
    # Even if 'packages' is prepended to sys.path, 'reva' must resolve to root 'reva/'
    repo_root = Path(__file__).resolve().parent.parent.parent
    packages_dir = repo_root / "packages"
    if str(packages_dir) not in sys.path:
        sys.path.insert(0, str(packages_dir))

    import reva
    expected_root_reva = repo_root / "reva" / "__init__.py"
    actual_reva_file = Path(reva.__file__).resolve()

    assert actual_reva_file == expected_root_reva.resolve(), (
        f"reva.__file__ ({actual_reva_file}) must match root {expected_root_reva.resolve()}"
    )

    from reva import config
    assert hasattr(config, "RevaSettings")
    assert hasattr(config, "get_settings")
