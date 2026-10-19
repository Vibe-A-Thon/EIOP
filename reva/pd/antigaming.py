"""Anti-gaming static and dynamic validation rules AG-05, AG-06, AG-13, AG-14 (T-209 / REVA-PD-004)."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Any, List, Optional, Set, Union

from reva.pd.bindings import Binding, FixtureRef


def check_ag05_meaningful_assertion(func_ast: ast.AST) -> bool:
    """Verify test function contains at least one non-trivial assertion (AG-05)."""
    found_assertion = False

    for node in ast.walk(func_ast):
        # 1. Check `assert <test>`
        if isinstance(node, ast.Assert):
            # Flag trivial assertions like `assert True`, `assert 1`, `assert 1 == 1`
            if isinstance(node.test, (ast.Constant, ast.NameConstant)):
                continue
            if isinstance(node.test, ast.Compare):
                # Reject comparison between two constant literals
                if isinstance(node.test.left, (ast.Constant, ast.NameConstant)) and all(
                    isinstance(c, (ast.Constant, ast.NameConstant)) for c in node.test.comparators
                ):
                    continue
            found_assertion = True
            break

        # 2. Check context managers like `with pytest.raises(...)`, `with pytest.warns(...)`
        if isinstance(node, ast.With):
            for item in node.items:
                call = item.context_expr
                if isinstance(call, ast.Call):
                    func_name = ""
                    if isinstance(call.func, ast.Attribute):
                        func_name = call.func.attr
                    elif isinstance(call.func, ast.Name):
                        func_name = call.func.id
                    if func_name in ("raises", "warns"):
                        found_assertion = True
                        break
            if found_assertion:
                break

        # 3. Check unittest `self.assert*`, Jest/Playwright `expect(...)`, PyHamcrest `assertThat(...)`
        if isinstance(node, ast.Call):
            call_name = ""
            if isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                call_name = node.func.id

            if call_name.startswith("assert") and call_name not in ("assert_called", "assert_called_once", "assert_called_with"):
                found_assertion = True
                break
            if call_name in ("expect", "assertThat"):
                # Argument must not be a bare constant
                if node.args and not isinstance(node.args[0], (ast.Constant, ast.NameConstant)):
                    found_assertion = True
                    break

    return found_assertion


def check_ag06_no_self_mock(
    patched_targets: List[str],
    owner_symbols: List[str],
    func_ast: Optional[ast.AST] = None,
) -> bool:
    """Ensure test does not mock or patch the owner symbol under test (AG-06)."""
    norm_owners = [s.strip().lower() for s in owner_symbols if s.strip()]

    # Check dynamic targets recorded by pytest_plugin
    for pt in patched_targets:
        pt_lower = pt.strip().lower()
        for ow in norm_owners:
            if pt_lower == ow or pt_lower.endswith("." + ow) or ow.endswith("." + pt_lower):
                return False

    # Check static AST if provided
    if func_ast is not None:
        for node in ast.walk(func_ast):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    func_name = node.func.id

                # patch("qualified.path")
                if func_name == "patch":
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        val_lower = node.args[0].value.lower()
                        for ow in norm_owners:
                            if val_lower == ow or val_lower.endswith("." + ow) or ow.endswith("." + val_lower):
                                return False
                # patch.object(OwnerClass, "method")
                elif func_name == "object":
                    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
                        attr_val = node.args[1].value.lower()
                        for ow in norm_owners:
                            if attr_val == ow or ow.endswith("." + attr_val):
                                return False

    return True


def check_ag13_positive_test_count(test_count: int) -> bool:
    """Verify test count for the obligation is strictly greater than 0 (AG-13)."""
    return test_count > 0


def check_ag14_fixtures_integrity(
    fixtures: List[FixtureRef],
    repo_root: Union[str, Path],
) -> List[str]:
    """Verify each fixture file exists and matches its declared sha256 (AG-14)."""
    violations: List[str] = []
    root = Path(repo_root).resolve()

    for f in fixtures:
        fpath = root / f.path
        if not fpath.is_file():
            violations.append(f"Fixture file missing: {f.path}")
            continue

        if f.sha256:
            actual_digest = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if actual_digest != f.sha256.lower():
                violations.append(
                    f"Fixture sha256 mismatch for {f.path}: declared {f.sha256}, actual {actual_digest}"
                )

    return violations
