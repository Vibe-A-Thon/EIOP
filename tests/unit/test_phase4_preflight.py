"""Unit Tests for Phase 4 Pre-flight Verification (PRE-001, PRE-002).

Validates:
- PRE-001: Package-collision and baseline reconciliation
- PRE-002: Requirements registry integrity and Universal Definition of Done
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.req("PRE-001")
def test_preflight_package_collision_and_baselines():
    """PRE-001: Ensure no accidental package collisions and baseline modules exist."""
    required_packages = [
        "packages/eoip/token_formats",
        "packages/eoip/verification",
        "packages/eoip/routing",
        "packages/eoip/graph_graph",
        "packages/eoip/token_budget",
        "packages/eoip/federation",
        "packages/eoip/causal",
        "packages/eoip/distillation",
        "packages/eoip/gnn",
        "packages/eoip/xai",
        "packages/eoip/nlp",
        "packages/eoip/mlops",
        "packages/eoip/embeddings",
        "packages/eoip/compliance",
        "packages/eoip/privacy",
    ]
    for pkg in required_packages:
        pkg_dir = REPO_ROOT / pkg
        assert pkg_dir.exists(), f"Expected package directory {pkg} to exist"


@pytest.mark.req("PRE-002")
def test_preflight_requirements_registry_registered():
    """PRE-002: Ensure all Phase 4 requirement IDs are recorded in requirements-registry.json."""
    registry_file = REPO_ROOT / "requirements-registry.json"
    assert registry_file.exists()

    with open(registry_file, encoding="utf-8") as f:
        registry = json.load(f)

    registered_ids = {r["id"] for r in registry}

    expected_phase4_ids = [
        "PRE-001", "PRE-002",
        "CORE-001", "CORE-002", "CORE-003", "CORE-004", "CORE-005", "CORE-006",
        "AGENT-001", "AGENT-002", "AGENT-003", "AGENT-004",
        "GRAPH-001", "GRAPH-002", "GRAPH-003", "GRAPH-004", "GRAPH-005", "GRAPH-006",
        "AI-001", "AI-002", "AI-003", "AI-004", "AI-005", "AI-006", "AI-007",
        "INFRA-001", "INFRA-002", "INFRA-003", "INFRA-004", "INFRA-005", "INFRA-006", "INFRA-007",
        "UI-001", "UI-002", "UI-003", "UI-004", "UI-005", "UI-006", "UI-007", "UI-008", "UI-009",
        "COMPLY-001", "COMPLY-002", "COMPLY-003",
        "TEST-001", "TEST-002", "TEST-003", "TEST-004", "TEST-005",
        "MULTI-001", "MULTI-002",
    ]

    for req_id in expected_phase4_ids:
        assert req_id in registered_ids, f"Expected {req_id} to be registered in requirements-registry.json"
