"""Mark WP 6.1 (Platform and Ecosystem Moonshots) requirements as done."""

from _mark_done import mark_done

TEST_FILE = "tests/unit/test_platform_and_ecosystem_moonshots_wp61.py"

WP61_REQUIREMENTS = {
    "MS-6": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/moonshot/spatial_lod_canvas.py"],
    },
    "MS-7": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/moonshot/confidential_graph.py"],
    },
    "MS-11": {
        "test_file": TEST_FILE,
        "code_paths": [
            "packages/eoip/marketplace/manifest.py",
            "packages/eoip/marketplace/packager.py",
        ],
    },
    "MS-12": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/moonshot/collaborative_crdt.py"],
    },
    "MS-13": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ontology/gitops.py"],
    },
    "MS-16": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/process_mining.py"],
    },
    "MS-17": {
        "test_file": TEST_FILE,
        "code_paths": [
            "packages/eoip/agents/mesh_supervisor.py",
            "packages/eoip/agents/orchestration.py",
        ],
    },
    "MS-25": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ontology/domain_pack_manager.py"],
    },
    "MS-26": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/branding/theme.py"],
    },
    "MS-27": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/billing/metering.py"],
    },
    "G2-PM-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/process_mining.py"],
    },
    "G2-PM-003": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/process_mining.py"],
    },
    "G2-PM-004": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/process_mining.py"],
    },
    "G2-PM-005": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/process_mining.py"],
    },
}

if __name__ == "__main__":
    mark_done(WP61_REQUIREMENTS)
