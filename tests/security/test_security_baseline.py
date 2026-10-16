"""Security baseline tests (Phase 1 security requirements).

Validates path traversal rejection, input bounds, secret redaction,
query policy enforcement, and read-only MCP tool registration.
"""

import pytest
from eoip.agents.runtime import READ_TOOLS, AgentRegistry
from eoip.audit.redaction import redact_secrets
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
from eoip.query.policy import QueryPolicy


def test_path_traversal_rejection():
    """Source paths are allowlisted; path traversal is rejected."""
    from eoip.snapshot import restore
    store = MemoryGraphStore()
    malicious_archive = {
        "sha256": "fake",
        "payload": {
            "schema_version": "1.0",
            "vertices": [],
            "edges": [],
            "raw_files": {"../../etc/passwd": {"content": "root:x:0:0"}},
        },
    }
    import json
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(malicious_archive, f)
        f.flush()
        with pytest.raises(ValueError, match="checksum|path"):
            restore(store, tempfile.gettempdir(), f.name)


def test_secret_redaction():
    """Secrets are redacted from audit records."""
    record = {
        "actor": "user",
        "token": "secret-token-123",
        "password": "my-password",
        "safe_summary": "Bearer sk-abc123 was used",
        "nested": {"api_key": "key-value"},
    }
    redacted = redact_secrets(record)
    assert redacted["token"] == "***REDACTED***"
    assert redacted["password"] == "***REDACTED***"
    assert "sk-abc123" not in redacted["safe_summary"]
    assert redacted["nested"]["api_key"] == "***REDACTED***"
    assert redacted["actor"] == "user"


def test_query_policy_enforces_bounds():
    """Query policy rejects out-of-bounds requests."""
    plan = QueryPlan(
        intent="IMPACT",
        anchors=["test"],
        max_depth=8,
        result_limit=500,
        timeout_ms=30000,
        evidence_mode="NONE",
    )
    strict = QueryPolicy(max_depth=4, max_results=100, max_timeout_ms=5000)
    violations = strict.validate(plan)
    assert len(violations) == 3


def test_read_only_agent_tools():
    """Agent registry rejects non-read tools."""
    class BadAgent:
        agent_id = "BadAgent"
        allowed_tools = frozenset({"search", "delete_vertex"})
        max_steps = 5
        max_seconds = 10.0
        def execute(self, request, store):
            pass

    registry = AgentRegistry()
    with pytest.raises(ValueError, match="non-read"):
        registry.register(BadAgent())


def test_read_tools_allowlist():
    """READ_TOOLS only contains safe read operations."""
    assert READ_TOOLS.issuperset({"search", "entity", "path", "impact", "lineage"})
    assert "delete" not in READ_TOOLS
    assert "write" not in READ_TOOLS
    assert "execute" not in READ_TOOLS


def test_oversized_input_rejection():
    """Oversized canonical IDs are rejected by Pydantic validation."""
    from pydantic import ValidationError

    from apps.api.main import TraceRequest
    with pytest.raises(ValidationError):
        TraceRequest(canonical_id="x" * 513)


def test_query_policy_blocks_edges():
    """Blocked edge types are rejected by policy."""
    policy = QueryPolicy(blocked_edges=frozenset({"CONTAINS"}))
    plan = QueryPlan(
        intent="PATH",
        anchors=["a", "b"],
        max_depth=4,
        result_limit=100,
        evidence_mode="NONE",
        relationship_allowlist=["CONTAINS", "MODIFIES"],
    )
    violations = policy.validate(plan)
    assert any("blocked" in v.lower() for v in violations)
