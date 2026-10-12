"""Mark WP 5.2 Ontology GitOps and Marketplace requirements as done."""

from _mark_done import mark_done

WP52_REQUIREMENTS = {
    "GAP-GITOPS-002": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-GITOPS-003": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
            "apps/api/main.py",
        ],
    },
    "GAP-GITOPS-004": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-GITOPS-005": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-GITOPS-006": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-GITOPS-007": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-GITOPS-008": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/ontology/gitops.py",
            "packages/eoip/ontology/gitops_router.py",
        ],
    },
    "GAP-MKT-002": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/manifest.py",
            "packages/eoip/marketplace/packager.py",
        ],
    },
    "GAP-MKT-003": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/packager.py",
            "packages/eoip/marketplace/sample.py",
        ],
    },
    "GAP-MKT-004": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/installer.py",
            "packages/eoip/marketplace/packager.py",
        ],
    },
    "GAP-MKT-005": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/installer.py",
            "packages/eoip/marketplace/packager.py",
        ],
    },
    "GAP-MKT-006": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/installer.py",
            "packages/eoip/marketplace/registry.py",
        ],
    },
    "GAP-MKT-007": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/installer.py",
            "packages/eoip/marketplace/semver.py",
        ],
    },
    "GAP-MKT-008": {
        "test_file": "tests/unit/test_gitops_and_marketplace_wp52.py",
        "code_paths": [
            "packages/eoip/marketplace/signing.py",
            "packages/eoip/marketplace/registry.py",
        ],
    },
}

if __name__ == "__main__":
    mark_done(WP52_REQUIREMENTS)
