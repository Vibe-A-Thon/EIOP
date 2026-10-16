"""Mark WP 5.4 (VS Code Extension) and WP 5.5 (Enterprise Security) requirements as done."""

from _mark_done import mark_done

TEST_FILE_VSC = "tests/unit/test_vscode_extension_wp54.py"
TEST_FILE_SEC = "tests/unit/test_enterprise_security_wp55.py"

VSC_CODE_PATHS = [
    "apps/vscode-extension/extension.js",
    "apps/vscode-extension/package.json",
]

SEC_CODE_PATHS = [
    "packages/eoip/authz/tokens.py",
    "packages/eoip/authz/security_router.py",
    "apps/api/extended.py",
    "apps/web/src/admin/SecurityGovernanceDashboard.jsx",
]

WP54_AND_WP55_REQUIREMENTS = {
    "FR-VSCODE-001": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "FR-VSCODE-002": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-002": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-003": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-004": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-005": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-006": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-007": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "G2-VSC-008": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "MVP-FR-019": {
        "test_file": TEST_FILE_VSC,
        "code_paths": VSC_CODE_PATHS,
    },
    "GAP-SEC-008": {
        "test_file": TEST_FILE_SEC,
        "code_paths": SEC_CODE_PATHS,
    },
    "GAP-SEC-009": {
        "test_file": TEST_FILE_SEC,
        "code_paths": SEC_CODE_PATHS,
    },
    "GAP-SEC-010": {
        "test_file": TEST_FILE_SEC,
        "code_paths": SEC_CODE_PATHS,
    },
    "GAP-SEC-011": {
        "test_file": TEST_FILE_SEC,
        "code_paths": SEC_CODE_PATHS,
    },
    "GAP-SEC-012": {
        "test_file": TEST_FILE_SEC,
        "code_paths": SEC_CODE_PATHS,
    },
}

if __name__ == "__main__":
    mark_done(WP54_AND_WP55_REQUIREMENTS)
