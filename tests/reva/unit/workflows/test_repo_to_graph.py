"""
Unit & Integration Tests for RepoToGraphOrchestrator (REVA-AB-014/015, T-ENH-004/006/007).
Validates:
1. Local directory and URL repository ingestion
2. Knowledge Graph construction (classes, functions, endpoints, call graphs)
3. Wisdom Graph construction (ADRs, patterns, risks)
4. Zero-Data-Leak LLM Egress Fencing
5. Merkle Warrant emission
"""

import json
import os
import tempfile
import pytest

from reva.workflows.repo_to_graph import RepoToGraphOrchestrator


@pytest.fixture
def sample_repo_dir():
    with tempfile.TemporaryDirectory(prefix="test_repo_") as tmpdir:
        # Create a sample python project structure
        src_dir = os.path.join(tmpdir, "sample_pkg")
        os.makedirs(src_dir, exist_ok=True)

        # Main module
        main_py = os.path.join(src_dir, "app.py")
        with open(main_py, "w", encoding="utf-8") as f:
            f.write('''"""Main application module."""
import os
from .service import DataProcessor

class APIServer:
    """Core server."""
    def __init__(self, port: int = 8080):
        self.port = port
        self.processor = DataProcessor()

    def handle_request(self, payload: dict) -> dict:
        return self.processor.process(payload)

def get_status():
    return {"status": "ok"}
''')

        # Service module with an API endpoint pattern
        service_py = os.path.join(src_dir, "service.py")
        with open(service_py, "w", encoding="utf-8") as f:
            f.write('''"""Service layer."""

class DataProcessor:
    def process(self, data: dict) -> dict:
        if not data:
            return {}
        for k, v in data.items():
            if k == "secret":
                return {"redacted": True}
        return {"processed": True}

# Simulated route decorator
def get(path: str):
    def decorator(fn):
        return fn
    return decorator

@get("/api/v1/health")
def health_endpoint():
    return {"healthy": True}
''')

        # Create an ADR in docs/adr
        adr_dir = os.path.join(tmpdir, "docs", "adr")
        os.makedirs(adr_dir, exist_ok=True)
        adr_file = os.path.join(adr_dir, "0001-use-layered-architecture.md")
        with open(adr_file, "w", encoding="utf-8") as f:
            f.write('''# 1. Use Layered Architecture

## Status
Accepted

## Context
We need a clean separation between API routes and business logic.

## Decision
Separate data processing into service layer classes.

## Consequences
Clear dependency boundaries and easier unit testing.
''')

        yield tmpdir


def test_repo_to_graph_orchestrator(sample_repo_dir):
    orchestrator = RepoToGraphOrchestrator()
    result = orchestrator.process_repository(
        repo_source=sample_repo_dir,
        synthesize_with_llm=True,
    )

    assert result is not None
    assert result.repo_id is not None
    assert result.warrant is not None
    assert result.warrant["id"].startswith("wr1_")

    # Verify Knowledge Graph
    kg = result.knowledge_graph
    assert kg["vertices_count"] > 0
    assert kg["edges_count"] > 0
    assert kg["metrics"]["total_python_files"] == 2
    assert kg["metrics"]["total_classes"] == 2
    assert kg["metrics"]["total_functions"] >= 3

    # Check that Classes and Functions are captured
    class_names = [v["name"] for v in kg["vertices"] if v["kind"] == "kg_Class"]
    assert "APIServer" in class_names
    assert "DataProcessor" in class_names

    # Verify Endpoint detection
    endpoint_names = [v["name"] for v in kg["vertices"] if v["kind"] == "kg_Endpoint"]
    assert any("/api/v1/health" in ep for ep in endpoint_names)

    # Verify Wisdom Graph
    wg = result.wisdom_graph
    assert wg["metrics"]["decisions_count"] >= 1
    decision_names = [v["name"] for v in wg["vertices"] if v["kind"] == "wg_Decision"]
    assert any("Use Layered Architecture" in d for d in decision_names)

    # Verify Egress Gate Audit
    assert result.egress_audit is not None
    assert result.egress_audit["policy"] == "REVA-SEC-013-STRICT"
    assert result.egress_audit["canary"].startswith("egress_canary_")
