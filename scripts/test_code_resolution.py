"""Resolve code paths from test imports for all TEST_NO_CODE requirements
"""
import ast
from pathlib import Path
import json

ROOT = Path(".").resolve()

def get_test_imports(test_file: str) -> list[str]:
    tf_path = ROOT / test_file
    if not tf_path.exists():
        return []
    content = tf_path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(content)
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name.startswith("eoip.") or n.name.startswith("apps."):
                    modules.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and (node.module.startswith("eoip.") or node.module.startswith("apps.")):
                modules.append(node.module)
    
    # Resolve to files
    resolved = []
    for mod in modules:
        parts = mod.split(".")
        if parts[0] == "eoip":
            base = ROOT / "packages" / "eoip" / "/".join(parts[1:])
            cand1 = base.with_suffix(".py")
            cand2 = base / "__init__.py"
            if cand1.exists():
                resolved.append(str(cand1.relative_to(ROOT)).replace("\\", "/"))
            elif cand2.exists():
                resolved.append(str(cand2.relative_to(ROOT)).replace("\\", "/"))
        elif parts[0] == "apps":
            base = ROOT / "apps" / "/".join(parts[1:])
            cand1 = base.with_suffix(".py")
            cand2 = base / "__init__.py"
            if cand1.exists():
                resolved.append(str(cand1.relative_to(ROOT)).replace("\\", "/"))
            elif cand2.exists():
                resolved.append(str(cand2.relative_to(ROOT)).replace("\\", "/"))
    return list(dict.fromkeys(resolved))

# Test on a few files
for tf in ["tests/unit/test_cp_registry.py", "tests/unit/test_code_parser.py", "tests/unit/test_github_connector.py", "tests/unit/test_gitlab_connector.py"]:
    print(tf, "->", get_test_imports(tf))
