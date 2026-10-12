"""Mark WP 7.1 (Scale and Polish) requirements as done."""

from _mark_done import mark_done

TEST_FILE = "tests/unit/test_scale_and_polish_wp71.py"

WP71_REQUIREMENTS = {
    "S-01": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/kgr/rendering/WebGLGraphRenderer.js",
            "apps/web/src/kgr/workers/layoutWorker.js",
            "apps/web/src/kgr/components/VisualQueryBuilder.jsx",
        ],
    },
    "S-02": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/benchmark.py"],
    },
    "S-03": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ci/pipeline.py", ".github/workflows/ci.yml"],
    },
    "S-04": {
        "test_file": TEST_FILE,
        "code_paths": [
            "docs/getting-started.md",
            "docs/architecture-guide.md",
            "docs/api-reference.md",
        ],
    },
    "S-05": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/security/hardening.py"],
    },
}

if __name__ == "__main__":
    mark_done(WP71_REQUIREMENTS)
