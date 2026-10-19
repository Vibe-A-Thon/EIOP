#!/usr/bin/env python3
"""Check that all tests under tests/reva/<depth>/ carry matching depth markers (T-002)."""

import ast
import sys
from pathlib import Path

VALID_DEPTHS = {"unit", "component", "integration", "acceptance", "conformance", "evaluation", "perf"}

def check_test_file(path: Path, expected_depth: str) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text, filename=str(path))
    except Exception as exc:
        return [f"{path}: parse error: {exc}"]

    # Check for module-level pytestmark
    has_module_mark = False
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "pytestmark":
                    # Check if expected_depth is referenced
                    if expected_depth in ast.unparse(node.value):
                        has_module_mark = True

    if has_module_mark:
        return []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_"):
                # Check decorators
                has_mark = False
                for dec in node.decorator_list:
                    dec_str = ast.unparse(dec)
                    if "reva_depth" in dec_str and expected_depth in dec_str:
                        has_mark = True
                        break
                if not has_mark:
                    errors.append(f"{path}:{node.lineno} test '{node.name}' lacks @pytest.mark.reva_depth('{expected_depth}')")

    return errors

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    tests_reva = repo_root / "tests" / "reva"
    if not tests_reva.exists():
        print("tests/reva does not exist yet.", file=sys.stderr)
        return 0

    all_errors = []
    for depth_dir in tests_reva.iterdir():
        if depth_dir.is_dir() and depth_dir.name in VALID_DEPTHS:
            for test_file in depth_dir.rglob("test_*.py"):
                all_errors.extend(check_test_file(test_file, depth_dir.name))

    if all_errors:
        print("Check depth markers FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("Check depth markers: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
