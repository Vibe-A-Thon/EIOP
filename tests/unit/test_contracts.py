import json
from pathlib import Path

from eoip.contracts import (
    AgentRequest,
    AgentResult,
    AuditEvent,
    Evidence,
    GraphMutation,
    GraphResult,
    MemoryRecord,
    NormalizedEntity,
    NormalizedRelationship,
    QueryPlan,
    RetrievalResult,
    SourceEvent,
    ToolRequest,
    ToolResult,
)

CONTRACTS = {
    "agent_request": AgentRequest,
    "agent_result": AgentResult,
    "audit_event": AuditEvent,
    "evidence": Evidence,
    "graph_mutation": GraphMutation,
    "graph_result": GraphResult,
    "memory_record": MemoryRecord,
    "normalized_entity": NormalizedEntity,
    "normalized_relationship": NormalizedRelationship,
    "query_plan": QueryPlan,
    "retrieval_result": RetrievalResult,
    "source_event": SourceEvent,
    "tool_request": ToolRequest,
    "tool_result": ToolResult,
}


def test_source_event_contract_imports_and_sets_capture_time() -> None:
    event = SourceEvent(
        event_id="event-1",
        source_system="jira",
        source_record_id="EOIP-1",
        payload_hash="abc123",
        payload={"key": "EOIP-1"},
    )

    assert event.captured_at.endswith("Z")


def test_audit_event_timestamp_uses_a_per_instance_factory() -> None:
    assert AuditEvent.model_fields["timestamp"].default_factory is not None


def test_runtime_contract_fields_match_checked_in_json_schemas() -> None:
    schema_root = Path(__file__).resolve().parents[2] / "schemas"
    for name, contract in CONTRACTS.items():
        schema = json.loads((schema_root / f"{name}.schema.json").read_text(encoding="utf-8"))
        assert set(schema["properties"]) == set(contract.model_fields), name
