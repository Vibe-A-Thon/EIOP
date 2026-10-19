"""Check imports in the test files for the 22 capabilities
"""
import ast
from pathlib import Path

ROOT = Path(".").resolve()

test_files = [
    "tests/unit/test_named_graph.py",
    "tests/unit/test_g2_readiness.py",
    "tests/unit/test_parallel_multihop.py",
    "tests/unit/test_ontology_packages.py",
    "tests/unit/test_query_intelligence.py",
    "tests/unit/test_unified_query_api.py",
    "tests/unit/test_splink_er_engine.py",
    "tests/unit/test_ontology_drift_review.py",
    "tests/unit/test_retrieval_vector.py"
]

for tf in test_files:
    p = ROOT / tf
    if not p.exists():
        print(f"MISSING: {tf}")
        continue
    content = p.read_text(encoding="utf-8")
    tree = ast.parse(content)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    print(f"\n{tf} imports:")
    for imp in list(dict.fromkeys(imports)):
        if "eoip" in imp or "apps" in imp:
            print(f"  - {imp}")
