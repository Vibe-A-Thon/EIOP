"""Mark WP 8.1 (Production Release Gate) requirements as done."""

from _mark_done import mark_done

TEST_FILE = "tests/unit/test_production_release_gate_wp8.py"

WP8_REQUIREMENTS = {
    "CG-GAP-008": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "docs/release-checklist.md"],
    },
    "REL-01": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "docs/release-checklist.md"],
    },
    "REL-02": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "packages/eoip/ci/pipeline.py"],
    },
    "REL-03": {
        "test_file": TEST_FILE,
        "code_paths": ["scripts/gap_coverage.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-04": {
        "test_file": TEST_FILE,
        "code_paths": ["scripts/check_product_gate.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-05": {
        "test_file": TEST_FILE,
        "code_paths": ["scripts/documentation_audit.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-06": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "packages/eoip/connectors/"],
    },
    "REL-07": {
        "test_file": TEST_FILE,
        "code_paths": ["scripts/setup_hubble.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-08": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "apps/web/src/"],
    },
    "REL-09": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py", "apps/vscode-extension/src/"],
    },
    "REL-10": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ha.py", "packages/eoip/snapshot.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-11": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/security/hardening.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-12": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/benchmark.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-13": {
        "test_file": TEST_FILE,
        "code_paths": ["scripts/check_markdown_links.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-14": {
        "test_file": TEST_FILE,
        "code_paths": ["tests/e2e/test_demo_flow.py", "packages/eoip/verification/release_gate.py"],
    },
    "REL-15": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/verification/release_gate.py"],
    },
    "MVP-FR-028": {
        "test_file": TEST_FILE,
        "code_paths": ["tests/e2e/test_demo_flow.py", "packages/eoip/demo.py"],
    },
}

if __name__ == "__main__":
    mark_done(WP8_REQUIREMENTS)
