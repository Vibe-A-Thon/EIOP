import sys
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))
from _mark_done import mark_done

entries = {
    "GAP-APP": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/dashboards/builder.py"],
    },
    "GAP-CATALOG": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/catalog/products.py"],
    },
    "GAP-GOV": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/ontology/stewardship.py"],
    },
    "GAP-HA": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/ha.py"],
    },
    "GAP-IDE": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["apps/vscode-extension/extension.js"],
    },
    "GAP-NOCODE": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/ontology/studio.py"],
    },
    "GAP-TEMPLATE": {
        "test_file": "tests/unit/test_enterprise_readiness_wp51.py",
        "code_paths": ["packages/eoip/ontology/industry_templates.py"],
    },
}

mark_done(entries)
print("WP 5.1 all 7 tasks marked done and synced successfully!")
